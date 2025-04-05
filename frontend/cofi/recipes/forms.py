# recipes/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'prep_time', 'cook_time', 'servings']

class IngredientForm(forms.ModelForm):
  name = forms.CharField(label='Zutat') # Hinzugefügt
  class Meta:
    model = Ingredient
    fields = ['quantity'] # openfoodfacts_id wird hier nicht angezeigt

IngredientFormSet = inlineformset_factory(Recipe, Ingredient,
                                        form=IngredientForm, # Verwende das neue IngredientForm
                                        extra=1, can_delete=True)