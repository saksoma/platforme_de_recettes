from django.shortcuts import render
from django.views import View

from recettes.views import add_favorite_flags, recipes_with_stats


class HomeView(View):
    def get(self, request):
        featured_recipes = recipes_with_stats(public=True).filter(is_featured=True).order_by("-created_at")[:6]
        add_favorite_flags(featured_recipes, request.user)
        return render(request, 'base/home.html', {'featured_recipes': featured_recipes})
