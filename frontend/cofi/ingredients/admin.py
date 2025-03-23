# /home/heinrich/projects/ConsciousFit/frontend/cofi/ingredients/admin.py

from django.contrib import admin
from .models import Ingredient, Allergen, Disease, IngredientImage, HouseholdMeasurement, IngredientHouseholdMeasurement

class IngredientImageInline(admin.TabularInline):
    model = IngredientImage
    extra = 1

class IngredientHouseholdMeasurementInline(admin.TabularInline):
    model = IngredientHouseholdMeasurement
    extra = 1

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_quantity', 'reference_unit', 'kcal', 'fat', 'protein', 'carbohydrates', 'sodium', 'fiber', 'vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k')
    search_fields = ('name',)
    filter_horizontal = ('allergens', 'not_recommended_for', 'can_cause')
    inlines = [IngredientImageInline, IngredientHouseholdMeasurementInline]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Allergen)
admin.site.register(Disease)
admin.site.register(HouseholdMeasurement)
