from django.urls import path

from .views import (
    MyRecipesView,
    RecipeCreateView,
    RecipeDetailView,
    RecipeEditView,
    RecipeListView,
    add_comment,
    delete_recipe,
    favorite_toggle,
    rate_recipe,
    remove_menu_item,
    weekly_menu,
)

app_name = "recettes"

urlpatterns = [
    path("", RecipeListView.as_view(), name="home"),
    path("create/", RecipeCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", RecipeEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", delete_recipe, name="delete"),
    path("my/", MyRecipesView.as_view(), name="my_recipes"),
    path("menu/", weekly_menu, name="weekly_menu"),
    path("menu/remove/<int:pk>/", remove_menu_item, name="remove_menu_item"),
    path("favorite/<int:pk>/", favorite_toggle, name="favorite_toggle"),
    path("rate/<int:pk>/", rate_recipe, name="rate"),
    path("search/", RecipeListView.as_view(), name="search"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="detail"),
    path("<int:pk>/comment/", add_comment, name="add_comment"),
]
