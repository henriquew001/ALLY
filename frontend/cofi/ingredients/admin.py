# /home/heinrich/projects/ConsciousFit/frontend/cofi/ingredients/admin.py

from django.contrib import admin
from .models import Ingredient

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'kcal', 'fat', 'protein', 'sugar')
    search_fields = ('name',)

admin.site.register(Ingredient, IngredientAdmin)
