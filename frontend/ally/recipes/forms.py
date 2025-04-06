# forms.py (Corrected Version - Using English Default Errors)

from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Recipe, Ingredient

# --- RecipeForm (Generally okay, ensure fields/exclude match your needs) ---
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # List the fields you want the user to edit
        fields = ['name', 'description', 'instructions', 'prep_time', 'cook_time', 'servings']
        # Or exclude fields set automatically (like author, created_at)
        # exclude = ['author']


# --- IngredientForm (Corrected) ---
class IngredientForm(forms.ModelForm):
    # Define fields explicitly to ensure required=True is enforced reliably.
    # By omitting 'error_messages', Django's default English messages will be used.
    name = forms.CharField(
        required=True
    )
    quantity = forms.CharField(
        required=True
    )

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity'] # Specify fields explicitly

    # REMOVED the custom clean() method as field-level validation is preferred here.


# --- BaseIngredientFormSet (Kept for potential future use) ---
class BaseIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # No custom formset-level validation added yet.
        pass


# --- IngredientFormSet Definition (Generally okay) ---
IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm, # Uses the corrected IngredientForm
    formset=BaseIngredientFormSet, # Uses the custom base formset
    extra=1, # Number of empty forms to display
    can_delete=True, # Allows users to mark ingredients for deletion
    # Consider adding min_num=1, validate_min=True if you require at least one ingredient
)