from django.contrib import admin
from .models import Recipe, Ingredient

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    fields = ['name', 'quantity'] # add quantity

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('name', 'created_at', 'updated_at', 'author') # add author
    search_fields = ('name', 'description')

admin.site.register(Recipe, RecipeAdmin)
