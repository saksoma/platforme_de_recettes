
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from .models import Tag
from .forms import TagForm
from recettes.models import Recipe
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_staff or user.is_superuser

def tag_list(request):
    tags = Tag.objects.annotate(recipe_count=Count('recipes')).order_by('name')
    return render(request, 'tag/list.html', {'tags': tags, 'total_tags': tags.count()})

@login_required(login_url='users:login')
@user_passes_test(is_admin)
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'Tag "{tag.name}" created.')
            return redirect('tag:list')
        messages.error(request, 'Please fix the errors.')
    else:
        form = TagForm()
    return render(request, 'tag/form.html', {'form': form, 'title': 'Create Tag', 'button_text': 'Create'})

@login_required(login_url='users:login')
@user_passes_test(is_admin)
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tag "{tag.name}" updated.')
            return redirect('tag:list')
        messages.error(request, 'Please fix the errors.')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tag/form.html', {'form': form, 'tag': tag, 'title': f'Edit Tag: {tag.name}', 'button_text': 'Update'})

@login_required(login_url='users:login')
@user_passes_test(is_admin)
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    recipes = Recipe.objects.filter(tags=tag)
    if request.method == 'POST':
        name = tag.name
        tag.delete()
        messages.success(request, f'Tag "{name}" deleted.')
        return redirect('tag:list')
    return render(request, 'tag/delete.html', {'tag': tag, 'recipes': recipes, 'recipe_count': recipes.count()})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    recipes_qs = Recipe.objects.filter(tags=tag).select_related('category','author').prefetch_related('tags')
    paginator = Paginator(recipes_qs, 12)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'tag/detail.html', {'tag': tag, 'recipes': recipes, 'recipe_count': paginator.count})
