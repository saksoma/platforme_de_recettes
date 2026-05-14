from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View

from category.models import Category
from tag.models import Tag

from .forms import RecipeForm, WeeklyMenuForm
from .models import Comment, Favorite, Rating, Recipe, WeeklyMenu


def recipes_with_stats(public=True):
    queryset = (
        Recipe.objects.select_related("author", "category")
        .prefetch_related("tags")
        .annotate(
            average_rating=Avg("ratings__score"),
            ratings_count=Count("ratings", distinct=True),
        )
    )
    if public:
        queryset = queryset.filter(status="approved")
    return queryset


def add_favorite_flags(recipes, user):
    if not user.is_authenticated:
        return

    recipe_ids = [recipe.pk for recipe in recipes]
    favorite_ids = set(
        Favorite.objects.filter(user=user, recipe_id__in=recipe_ids).values_list(
            "recipe_id", flat=True
        )
    )

    for recipe in recipes:
        recipe.is_favorite = recipe.pk in favorite_ids


def current_week_start():
    today = date.today()
    return today - timedelta(days=today.weekday())


class RecipeListView(View):
    template_name = "recettes/list.html"
    paginate_by = 9

    def get(self, request):
        recipes = recipes_with_stats(public=True)
        active_filters = []

        query = request.GET.get("q", "").strip()
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(ingredients__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()
            active_filters.append(f"Recherche: {query}")

        category_ids = request.GET.getlist("category")
        if category_ids:
            recipes = recipes.filter(category_id__in=category_ids)
            active_filters.append("Categories")

        prep_time = request.GET.get("prep_time")
        if prep_time == "0-15":
            recipes = recipes.filter(preparation_time__lt=15)
            active_filters.append("Moins de 15 min")
        elif prep_time == "15-30":
            recipes = recipes.filter(preparation_time__gte=15, preparation_time__lte=30)
            active_filters.append("15 - 30 min")
        elif prep_time == ">30":
            recipes = recipes.filter(preparation_time__gt=30)
            active_filters.append("Plus de 30 min")

        difficulties = request.GET.getlist("difficulty")
        if difficulties:
            recipes = recipes.filter(difficulty__in=difficulties)
            active_filters.append("Difficulte")

        tag_ids = request.GET.getlist("tags")
        if tag_ids:
            recipes = recipes.filter(tags__id__in=tag_ids).distinct()
            active_filters.append("Tags")

        if request.GET.get("sort") == "popular":
            recipes = recipes.order_by("-ratings_count", "-average_rating", "-created_at")
        else:
            recipes = recipes.order_by("-created_at")

        paginator = Paginator(recipes, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))
        add_favorite_flags(page_obj.object_list, request.user)

        context = {
            "recipes": page_obj,
            "categories": Category.objects.annotate(count=Count("recipe")).order_by("name"),
            "tags": Tag.objects.all(),
            "active_filters": active_filters,
        }
        return render(request, self.template_name, context)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recettes/detail.html"
    context_object_name = "recipe"
    queryset = recipes_with_stats(public=False)

    def get_object(self, queryset=None):
        recipe = super().get_object(queryset)
        can_view_private = (
            self.request.user.is_authenticated
            and (self.request.user == recipe.author or self.request.user.is_staff)
        )
        if recipe.status != "approved" and not can_view_private:
            raise PermissionDenied
        add_favorite_flags([recipe], self.request.user)
        return recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        tag_ids = list(recipe.tags.values_list("id", flat=True))
        similar = recipes_with_stats(public=True).exclude(pk=recipe.pk)

        if tag_ids or recipe.category_id:
            similar = similar.filter(Q(category=recipe.category) | Q(tags__id__in=tag_ids)).distinct()

        context["approved_comments"] = recipe.comments.filter(status="approved").select_related("user")
        context["similar_recipes"] = similar.order_by("-ratings_count", "-created_at")[:3]
        context["user_rating"] = None
        if self.request.user.is_authenticated:
            context["user_rating"] = (
                Rating.objects.filter(recipe=recipe, user=self.request.user)
                .values_list("score", flat=True)
                .first()
            )
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recettes/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not self.request.user.is_staff:
            form.instance.status = "pending"
        messages.success(self.request, "Recette envoyee pour moderation.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recettes:my_recipes")


class RecipeEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recettes/edit.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.status = "pending"
        messages.success(self.request, "Recette modifiee et envoyee pour moderation.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recettes:my_recipes")


class MyRecipesView(LoginRequiredMixin, View):
    template_name = "recettes/my_recipes.html"
    paginate_by = 9

    def get(self, request):
        recipes = recipes_with_stats(public=False).filter(author=request.user).order_by("-created_at")
        paginator = Paginator(recipes, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get("page"))

        return render(request, self.template_name, {"recipes": page_obj})


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Recette supprimee avec succes.")
        return redirect("recettes:my_recipes")

    return render(request, "recettes/delete.html", {"recipe": recipe})


@login_required
def favorite_toggle(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, status="approved")
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)

    if not created:
        favorite.delete()

    is_favorite = created
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"is_favorite": is_favorite})

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("recettes:detail", pk=recipe.pk)


@login_required
def rate_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, status="approved")
    if request.method == "POST":
        try:
            score = int(request.POST.get("score", 0))
        except ValueError:
            score = 0

        if 1 <= score <= 5:
            Rating.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={"score": score},
            )
            messages.success(request, "Merci pour votre note.")
        else:
            messages.error(request, "La note doit etre entre 1 et 5.")

    return redirect("recettes:detail", pk=recipe.pk)


@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, status="approved")

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            status = "approved" if request.user.is_staff else "pending"
            Comment.objects.create(recipe=recipe, user=request.user, content=content, status=status)
            messages.success(request, "Commentaire envoye pour moderation.")

    return redirect("recettes:detail", pk=recipe.pk)


@login_required
def weekly_menu(request):
    week_start = current_week_start()
    week_days = [week_start + timedelta(days=index) for index in range(7)]

    if request.method == "POST":
        form = WeeklyMenuForm(request.POST)
        if form.is_valid():
            WeeklyMenu.objects.update_or_create(
                user=request.user,
                date=form.cleaned_data["date"],
                meal_type=form.cleaned_data["meal_type"],
                defaults={
                    "recipe": form.cleaned_data["recipe"],
                    "servings": form.cleaned_data["servings"],
                },
            )
            messages.success(request, "Recette ajoutee au menu.")
            return redirect("recettes:weekly_menu")
    else:
        form = WeeklyMenuForm(initial={"date": date.today(), "servings": 1})

    menu_items = (
        WeeklyMenu.objects.filter(user=request.user, date__range=(week_days[0], week_days[-1]))
        .select_related("recipe", "recipe__category")
        .order_by("date", "meal_type")
    )

    context = {
        "form": form,
        "week_days": week_days,
        "menu_items": menu_items,
        "meal_choices": WeeklyMenu.MEAL_CHOICES,
    }
    return render(request, "recettes/weekly_menu.html", context)


@login_required
def remove_menu_item(request, pk):
    menu_item = get_object_or_404(WeeklyMenu, pk=pk, user=request.user)
    if request.method == "POST":
        menu_item.delete()
        messages.success(request, "Element retire du menu.")
    return redirect("recettes:weekly_menu")
