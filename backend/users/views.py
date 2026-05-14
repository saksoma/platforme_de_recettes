from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .forms import LoginForm, SignUpForm, UserProfileForm
from .models import UserProfile
from recettes.models import Recipe, Favorite, Comment


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('base:home')
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base:home')
            else:
                form.add_error(None, 'Identifiants invalides.')
        return render(request, 'users/login.html', {'form': form})


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('base:home')
        form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create user profile
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('base:home')
        return render(request, 'users/signup.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('base:home')


@login_required(login_url='users:login')
def profile_view(request, username=None):
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user

    profile = UserProfile.objects.get_or_create(user=user)[0]
    my_recipes = Recipe.objects.filter(author=user).select_related('category').prefetch_related('tags').order_by('-created_at')
    favorites = Favorite.objects.filter(user=user).select_related('recipe__category').order_by('-id')
    
    stats = {
        'recipes_count': my_recipes.count(),
        'favorites_count': favorites.count(),
        'comments_count': Comment.objects.filter(user=user).count(),
        'ratings_count': user.rating_set.count() if hasattr(user, 'rating_set') else 0,
    }

    context = {
        'profile_user': user,
        'profile': profile,
        'my_recipes': my_recipes[:6],
        'favorites': favorites[:6],
        'stats': stats,
        'is_own_profile': (request.user == user)
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='users:login')
def edit_profile(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
