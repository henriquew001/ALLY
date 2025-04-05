# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipe_list, name='recipe_list'), # Zeigt eine Liste aller Rezepte
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'), # Zeigt ein einzelnes Rezept
    path('recipes/new/', views.recipe_new, name='recipe_new'), # Erstellt ein neues Rezept
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'), # Bearbeitet ein Rezept
    path('recipes/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'), # Löscht ein Rezept
    path('recipes/ingredients/autocomplete/', views.ingredient_autocomplete, name='ingredient_autocomplete'),path('recipes/ingredients/autocomplete/', views.ingredient_autocomplete, name='ingredient_autocomplete'),
]
