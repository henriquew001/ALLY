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
    name = forms.CharField(label='Zutat')  # Hinzugefügt
    class Meta:
        model = Ingredient
        fields = ['name']  # openfoodfacts_id wird hier nicht angezeigt

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['quantity']

class BaseIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data.get('name') == '':
                raise forms.ValidationError("Bitte fülle alle Felder aus.")

IngredientFormSet = inlineformset_factory(Recipe, Ingredient,
                                        form=IngredientForm, # Verwende das neue IngredientForm
                                        extra=1, can_delete=True, formset=BaseIngredientFormSet)
