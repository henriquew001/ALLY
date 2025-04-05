# recipes/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient
from django.forms.models import BaseInlineFormSet

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'prep_time', 'cook_time', 'servings']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

class BaseIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('name') and not form.cleaned_data.get('quantity'):
                continue # ignore empty forms
            if form.cleaned_data and not form.cleaned_data.get('name'):
                raise forms.ValidationError("Bitte fülle alle Felder aus.")
            if form.cleaned_data and not form.cleaned_data.get('quantity'):
                raise forms.ValidationError("Bitte fülle alle Felder aus.")

IngredientFormSet = inlineformset_factory(Recipe, Ingredient,
                                        form=IngredientForm,
                                        extra=1, formset=BaseIngredientFormSet)
