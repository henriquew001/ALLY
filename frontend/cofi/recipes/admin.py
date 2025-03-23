# /home/heinrich/projects/ConsciousFit/frontend/cofi/recipes/admin.py

from django.contrib import admin
from .models import Recipe, DishIngredient
from django import forms
from ingredients.models import HouseholdMeasurement  # Import HouseholdMeasurement

class DishIngredientForm(forms.ModelForm):
    class Meta:
        model = DishIngredient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if self.instance is already saved in the database
        if self.instance.pk:
            if self.instance.ingredient:
                self.fields['household_measurement'].queryset = self.instance.ingredient.household_measurements.all()
        else:
            # If it's a new instance, set an empty queryset initially
            self.fields['household_measurement'].queryset = HouseholdMeasurement.objects.none()

class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1
    raw_id_fields = ('ingredient',)
    readonly_fields = ('unit',)
    form = DishIngredientForm

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_example')
    list_filter = ('is_example',)
    search_fields = ('title',)
    exclude = ('slug',)
    inlines = [DishIngredientInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(DishIngredient)
