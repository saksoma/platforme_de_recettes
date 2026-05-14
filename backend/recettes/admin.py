from django.contrib import admin

from .models import Comment, Favorite, Rating, Recipe, WeeklyMenu


@admin.action(description="Approuver les elements selectionnes")
def approve_items(modeladmin, request, queryset):
    queryset.update(status="approved")


@admin.action(description="Rejeter les elements selectionnes")
def reject_items(modeladmin, request, queryset):
    queryset.update(status="rejected")


@admin.action(description="Mettre en avant")
def feature_recipes(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Retirer de la mise en avant")
def unfeature_recipes(modeladmin, request, queryset):
    queryset.update(is_featured=False)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "is_featured",
        "difficulty",
        "servings",
        "created_at",
    )
    list_filter = ("status", "is_featured", "difficulty", "category", "tags")
    search_fields = ("title", "description", "ingredients", "author__username")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at",)
    actions = (approve_items, reject_items, feature_recipes, unfeature_recipes)
    fieldsets = (
        ("Contenu", {"fields": ("title", "description", "ingredients", "steps", "image")}),
        ("Organisation", {"fields": ("author", "category", "tags", "difficulty", "preparation_time", "servings")}),
        ("Nutrition", {"fields": ("calories", "protein", "carbs", "fat")}),
        ("Moderation", {"fields": ("status", "is_featured")}),
        ("Dates", {"fields": ("created_at",)}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("content", "user__username", "recipe__title")
    actions = (approve_items, reject_items)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "score")
    list_filter = ("score",)
    search_fields = ("recipe__title", "user__username")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__title")


@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "meal_type", "recipe", "servings")
    list_filter = ("date", "meal_type")
    search_fields = ("user__username", "recipe__title")
