from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-register/', views.user_register, name='user_register'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('update-recipe/<int:recipe_id>/', views.update_recipe, name='update_recipe'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('like-recipe/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
]
