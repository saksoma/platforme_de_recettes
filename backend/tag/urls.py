
from django.urls import path
from . import views

app_name = 'tag'

urlpatterns = [
    path('', views.tag_list, name='list'),
    path('create/', views.tag_create, name='create'),
    path('<int:pk>/edit/', views.tag_update, name='update'),
    path('<int:pk>/delete/', views.tag_delete, name='delete'),
    path('<slug:slug>/', views.tag_detail, name='detail'),
]
