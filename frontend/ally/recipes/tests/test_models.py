import pytest
from recipes.models import Recipe, Ingredient
from authentication.models import CustomUser  # Assuming this is where your user model is

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

@pytest.mark.django_db
@pytest.mark.unit
def test_recipe_creation(user):
    recipe = Recipe.objects.create(
        name='New Recipe',
        description='New Description',
        instructions='New Instructions',
        prep_time=15,
        cook_time=25,
        servings=6,
        author=user
    )
    assert Recipe.objects.count() == 1
    assert recipe.name == 'New Recipe'
    assert recipe.author == user

@pytest.mark.django_db
@pytest.mark.unit
def test_recipe_ingredient_relationship(recipe):
    assert recipe.ingredients.count() == 2
    ingredient1 = recipe.ingredients.first()
    assert ingredient1.name == 'Ingredient 1'
    assert ingredient1.quantity == '1 cup'

@pytest.mark.django_db
@pytest.mark.unit
def test_recipe_str(recipe):
    assert str(recipe) == 'Test Recipe'

@pytest.mark.django_db
@pytest.mark.unit
def test_ingredient_str(recipe):
    ingredient = recipe.ingredients.first()
    assert str(ingredient) == 'Ingredient 1'