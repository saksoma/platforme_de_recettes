from django.urls import path
from .views import profile_view, LoginView, SignUpView, LogoutView, edit_profile


app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', profile_view, name='profile_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


