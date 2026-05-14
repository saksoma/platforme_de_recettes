from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Category
from .forms import CategoryForm


def list_view(request):
    categories = Category.objects.all()
    # attach recipe_count if available via relationship - safe default 0
    for c in categories:
        c.recipe_count = getattr(c, 'recipe_count', 0)
    return render(request, 'category/list.html', {'categories': categories})


def is_admin(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category:list')
    else:
        form = CategoryForm()
    return render(request, 'category/create.html', {'form': form})


@user_passes_test(is_admin)
def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/update.html', {'form': form, 'category': category})


@user_passes_test(is_admin)
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        return redirect('category:list')
    return render(request, 'category/delete.html', {'category': category})