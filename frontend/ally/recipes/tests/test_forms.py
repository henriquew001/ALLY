import pytest
from recipes.forms import RecipeForm, IngredientFormSet
from recipes.models import Recipe
from django.utils import translation

@pytest.mark.django_db
@pytest.mark.unit
def test_recipe_form_valid_data():
    form_data = {
        'name': 'Test Recipe',
        'description': 'Test Description',
        'instructions': 'Test Instructions',
        'prep_time': 10,
        'cook_time': 20,
        'servings': 4,
    }
    form = RecipeForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
@pytest.mark.unit
def test_recipe_form_invalid_data():
    form_data = {
        'name': '',  # Missing name
        'description': 'Test Description',
        'instructions': 'Test Instructions',
        'prep_time': 10,
        'cook_time': 20,
        'servings': 4,
    }
    form = RecipeForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors

@pytest.mark.django_db
@pytest.mark.unit
def test_ingredient_formset_valid_data():
    # Erstelle ein Rezept
    recipe = Recipe.objects.create(
        name='Test Recipe',
        description='Test Description',
        instructions='Test Instructions',
        prep_time=10,
        cook_time=20,
        servings=4,
    )

    # Formulardaten mit einem gültigen Ingredient
    form_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-name': 'Ingredient A',
        'form-0-quantity': '100g',
    }

    formset = IngredientFormSet(data=form_data, instance=recipe, prefix='form')

    assert formset.is_valid()
    assert len(formset.forms) == 1
    assert formset.forms[0].is_valid()

@pytest.mark.django_db
@pytest.mark.unit
def test_ingredient_formset_invalid_data():
    recipe = Recipe.objects.create(
        name='Test',
        description='Test',
        instructions='Test',
        prep_time=10,
        cook_time=20,
        servings=2,
    )

    form_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-name': '',  # Missing name
        'form-0-quantity': '100g',
    }

    formset = IngredientFormSet(data=form_data, instance=recipe, prefix='form')

    assert not formset.is_valid()
    assert len(formset.forms) == 1

    # Check for the error on the 'name' field
    assert 'name' in formset.forms[0].errors
    assert formset.forms[0].errors['name'] == ['This field is required.']
    
@pytest.mark.django_db
@pytest.mark.unit
def test_ingredient_formset_missing_quantity():
    recipe = Recipe.objects.create(
        name='Test Recipe',
        description='Test Description',
        instructions='Test Instructions',
        prep_time=10,
        cook_time=20,
        servings=4,
    )

    form_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-name': 'test',
        'form-0-quantity': '',  # Missing quantity
    }

    formset = IngredientFormSet(data=form_data, instance=recipe, prefix='form')

    assert not formset.is_valid()
    assert len(formset.forms) == 1  # Ensure only one form is present

    # Check if the error is on the 'quantity' field
    assert 'quantity' in formset.forms[0].errors
    assert formset.forms[0].errors['quantity'] == ['This field is required.']
