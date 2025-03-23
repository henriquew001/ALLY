# /home/heinrich/projects/ConsciousFit/frontend/cofi/recipes/admin.py

from django.contrib import admin
from .models import Recipe, DishIngredient

class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_example')
    list_filter = ('is_example',)
    search_fields = ('title',)
    exclude = ('slug',)
    inlines = [DishIngredientInline]

admin.site.register(Recipe, RecipeAdmin)
