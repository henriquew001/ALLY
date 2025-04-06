from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'prep_time', 'cook_time', 'servings']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        quantity = cleaned_data.get('quantity')

        if not name:
            raise forms.ValidationError({'name': ['This field is required.']})

        if not quantity:
            raise forms.ValidationError({'quantity': ['This field is required.']})

        return cleaned_data


class BaseIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Here you can add additional formset-level validation if needed
        # For example, to ensure no empty ingredients are allowed
        pass

# InlineFormSet for the Recipe model and Ingredient model
IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    formset=BaseIngredientFormSet,
    extra=1,  # One extra form for adding new ingredients
    can_delete=False,  # Changed to False
)