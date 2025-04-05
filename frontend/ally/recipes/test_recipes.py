# recipes/test_recipes.py
import pytest
from django.urls import reverse
from .models import Recipe, Ingredient
from django.contrib.auth.models import User
from pymongo.errors import ConnectionFailure
from unittest.mock import patch
from authentication.models import CustomUser
from .forms import RecipeForm, IngredientFormSet
from bs4 import BeautifulSoup

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='testuser@example.com',  # Add the email here
        username='testuser',
        password='testpassword'
    )

@pytest.fixture
def recipe(user):
    recipe = Recipe.objects.create(
        name='Test Recipe',
        description='Test Description',
        instructions='Test Instructions',
        prep_time=10,
        cook_time=20,
        servings=4,
        author=user
    )
    Ingredient.objects.create(recipe=recipe, name='Ingredient 1', quantity='1 cup')
    Ingredient.objects.create(recipe=recipe, name='Ingredient 2', quantity='2 tbsp')
    return recipe

@pytest.mark.django_db
def test_recipe_creation(client, user):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_new')
    data = {
        'name': 'New Recipe',
        'description': 'New Description',
        'instructions': 'New Instructions',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 6,
        'ingredients-TOTAL_FORMS': '2',
        'ingredients-INITIAL_FORMS': '0',
        'ingredients-MIN_NUM_FORMS': '0',
        'ingredients-MAX_NUM_FORMS': '1000',
        'ingredients-0-name': 'Ingredient A',
        'ingredients-0-quantity': '100g',
        'ingredients-1-name': 'Ingredient B',
        'ingredients-1-quantity': '200ml',
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    # Check if the form is valid
    form = RecipeForm(data)
    ingredient_formset = IngredientFormSet(data, prefix='ingredients')
    if not form.is_valid() or not ingredient_formset.is_valid():
        print("Form errors:")
        print(form.errors)
        print("Ingredient formset errors:")
        print(ingredient_formset.errors)
    assert Recipe.objects.count() == 1
    assert Ingredient.objects.count() == 2
    recipe = Recipe.objects.first()
    assert recipe.name == 'New Recipe'
    assert recipe.author == user
    assert recipe.ingredients.count() == 2

@pytest.mark.django_db
def test_recipe_edit(client, user, recipe):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_edit', kwargs={'recipe_id': recipe.pk})
    data = {
        'name': 'Edited Recipe',
        'description': 'Edited Description',
        'instructions': 'Edited Instructions',
        'prep_time': 5,
        'cook_time': 10,
        'servings': 2,
        'ingredients-TOTAL_FORMS': '2',
        'ingredients-INITIAL_FORMS': '2',
        'ingredients-MIN_NUM_FORMS': '0',
        'ingredients-MAX_NUM_FORMS': '1000',
        'ingredients-0-id': recipe.ingredients.all()[0].id,
        'ingredients-0-name': 'Edited Ingredient 1',
        'ingredients-0-quantity': '50g',
        'ingredients-1-id': recipe.ingredients.all()[1].id,
        'ingredients-1-name': 'Edited Ingredient 2',
        'ingredients-1-quantity': '100ml',
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    recipe.refresh_from_db()
    assert recipe.name == 'Edited Recipe'
    assert recipe.ingredients.count() == 2
    assert recipe.ingredients.all()[0].name == 'Edited Ingredient 1'

@pytest.mark.django_db
def test_recipe_delete(client, user, recipe):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_delete', kwargs={'recipe_id': recipe.pk})
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert Recipe.objects.count() == 0
    assert Ingredient.objects.count() == 0

@pytest.mark.django_db
def test_recipe_list_view(client, user, recipe):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'recipes' in response.context
    assert len(response.context['recipes']) == 1

@pytest.mark.django_db
def test_recipe_detail_view(client, user, recipe):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_detail', kwargs={'recipe_id': recipe.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'recipe' in response.context
    assert 'ingredients' in response.context
    assert response.context['recipe'] == recipe
    assert len(response.context['ingredients']) == 2

@pytest.mark.django_db
@patch('recipes.views.settings')
def test_ingredient_autocomplete_mongo_placeholder(mock_settings, client, user):
    client.login(username='testuser@example.com', password='testpassword')
    mock_settings.MONGO_CLIENT.admin.command.side_effect = ConnectionFailure
    url = reverse('recipes:ingredient_autocomplete')
    response = client.get(url, {'query': 'test'})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['name'] == 'Placeholder Ingredient 1'

@pytest.mark.django_db
def test_recipe_creation_validation(client, user):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_new')
    data = {
        'name': 'New Recipe',
        'description': 'New Description',
        'instructions': 'New Instructions',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 6,
        'ingredients-TOTAL_FORMS': '1',
        'ingredients-INITIAL_FORMS': '0',
        'ingredients-MIN_NUM_FORMS': '0',
        'ingredients-MAX_NUM_FORMS': '1000',
        'ingredients-0-name': '',
        'ingredients-0-quantity': '',
    }
    response = client.post(url, data, follow=False)
    assert response.status_code == 200
    assert Recipe.objects.count() == 0
    assert Ingredient.objects.count() == 0
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the error list
    error_list = soup.find('ul', class_='errorlist')
    # Check if the error list exists and contains the error message
    assert error_list is not None
    assert "Bitte fülle alle Felder aus." in error_list.text

@pytest.mark.django_db
def test_recipe_creation_validation_quantity(client, user):
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_new')
    data = {
        'name': 'New Recipe',
        'description': 'New Description',
        'instructions': 'New Instructions',
        'prep_time': 15,
        'cook_time': 25,
        'servings': 6,
        'ingredients-TOTAL_FORMS': '1',
        'ingredients-INITIAL_FORMS': '0',
        'ingredients-MIN_NUM_FORMS': '0',
        'ingredients-MAX_NUM_FORMS': '1000',
        'ingredients-0-name': 'test',
        'ingredients-0-quantity': '',
    }
    response = client.post(url, data, follow=False)
    assert response.status_code == 200
    assert Recipe.objects.count() == 0
    assert Ingredient.objects.count() == 0
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the error list
    error_list = soup.find('ul', class_='errorlist')
    # Check if the error list exists and contains the error message
    assert error_list is not None
    assert "Bitte fülle alle Felder aus." in error_list.text
