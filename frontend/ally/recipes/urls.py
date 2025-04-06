# recipes/urls.py
from django.urls import path
from . import views

app_name = 'recipes'  # Defines the namespace

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # No 'recipes/' prefix
    path('new/', views.recipe_new, name='recipe_new'),  # No 'recipes/' prefix
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # No 'recipes/' prefix
    path('<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),  # No 'recipes/' prefix
    path('<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),  # No 'recipes/' prefix
    path('ingredients/autocomplete/', views.ingredient_autocomplete, name='ingredient_autocomplete'),  # No 'recipes/' prefix
    path('debug-formset/', views.debug_formset_view, name='debug_formset'),
]
