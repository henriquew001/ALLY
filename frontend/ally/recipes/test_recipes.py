import pytest
from django.urls import reverse
from .models import Recipe, Ingredient
from authentication.models import CustomUser
from .forms import RecipeForm, IngredientFormSet
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

# Fixtures (no change needed - these are still useful for setup)
@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='testuser@example.com',
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

# Mock MongoDB Function (Keep this if you still need to test the autocomplete view)
def mock_mongo_client():
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_collection.find.return_value = []
    mock_client.food_data = MagicMock()
    mock_client.food_data.ingredients_en = mock_collection
    return mock_client

# Helper function to apply the MongoDB mock
def apply_mongo_mock(test_function):
    def wrapper(*args, **kwargs):
        with patch('recipes.views.settings.MONGO_CLIENT', new=mock_mongo_client()):
            test_function(*args, **kwargs)
    return wrapper

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
def test_recipe_creation_integration(client, user):
    """
    Integration test for recipe creation.
    Tests the interaction between the view, form, and model.
    """
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
    assert Recipe.objects.count() == 1
    assert Ingredient.objects.count() == 2
    recipe = Recipe.objects.first()
    assert recipe.name == 'New Recipe'
    assert recipe.author == user
    assert recipe.ingredients.count() == 2

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
def test_recipe_edit_integration(client, user, recipe):
    """
    Integration test for recipe editing.
    Tests the interaction between the view, form, and model during edit.
    """
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
@pytest.mark.integration
@pytest.mark.system
def test_recipe_delete_integration(client, user, recipe):
    """
    Integration test for recipe deletion.
    Tests the delete view and its effect on the model.
    """
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_delete', kwargs={'recipe_id': recipe.pk})
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert Recipe.objects.count() == 0
    assert Ingredient.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
def test_recipe_list_view_integration(client, user, recipe):
    """
    Integration test for the recipe list view.
    Checks if the view correctly retrieves and displays recipes.
    """
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'recipes' in response.context
    assert len(response.context['recipes']) == 1

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
def test_recipe_detail_view_integration(client, user, recipe):
    """
    Integration test for the recipe detail view.
    Checks if the view correctly retrieves and displays a single recipe.
    """
    client.login(username='testuser@example.com', password='testpassword')
    url = reverse('recipes:recipe_detail', kwargs={'recipe_id': recipe.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'recipe' in response.context
    assert 'ingredients' in response.context
    assert response.context['recipe'] == recipe
    assert len(response.context['ingredients']) == 2

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
@patch('recipes.views.settings')
def test_ingredient_autocomplete_mongo_integration(mock_settings, client, user):
    """
    Integration test for ingredient autocomplete.
    Tests the view's interaction with the MongoDB (or mock).
    """
    client.login(username='testuser@example.com', password='testpassword')
    mock_collection = MagicMock()
    mock_collection.find.return_value = []  # Simulate no results
    mock_settings.MONGO_CLIENT.food_data.ingredients_en = mock_collection

    url = reverse('recipes:ingredient_autocomplete')
    response = client.get(url, {'query': 'test'})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
def test_recipe_creation_validation_integration(client, user):
    """
    Integration test for recipe creation with validation errors.
    Ensures that validation errors are correctly handled and displayed.
    """
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
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Recipe.objects.count() == 0
    assert Ingredient.objects.count() == 0
    soup = BeautifulSoup(response.content, 'html.parser')
    error_list = soup.find('ul', class_='errorlist')
    assert error_list is not None
    assert "Bitte fülle alle Felder aus." in error_list.text
    form = soup.find('form')
    assert form is not None

@pytest.mark.django_db
@pytest.mark.integration
@pytest.mark.system
def test_recipe_creation_validation_quantity_integration(client, user):
    """
    Integration test for recipe creation with missing quantity.
    Specifically tests the ingredient form validation.
    """
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
    soup = BeautifulSoup(response.content, 'html.parser')
    error_list = soup.find('ul', class_='errorlist')
    assert error_list is not None
    assert "Bitte fülle alle Felder aus." in error_list.text
    form = soup.find('form')
    assert form is not None