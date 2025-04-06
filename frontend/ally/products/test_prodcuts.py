import pytest
from django.urls import reverse
from django.test import Client
from products.models import ProductType, Product, RecipeContent, VideoContent, DocumentContent, ProductItem
from recipes.models import Recipe
from django.contrib.contenttypes.models import ContentType

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def product_type():
    return ProductType.objects.create(name="Test Type", description="Test Description")

@pytest.fixture
def recipe():
    return Recipe.objects.create(
        name="Test Recipe",
        description="Test Recipe",
        instructions="Test Instructions",
        prep_time=30,
        cook_time=60,
        servings=4,
    )

@pytest.fixture
def product(product_type):
    return Product.objects.create(
        title="Test Product",
        description="Test Product Description",
        price=19.99,
        type=product_type,
    )

@pytest.mark.unit
@pytest.mark.system
@pytest.mark.integration
@pytest.mark.django_db
def test_product_recipe_relationship(product, recipe):
    recipe_content = RecipeContent.objects.create(recipe=recipe)
    ProductItem.objects.create(product=product, content_object=recipe_content)

    # Get the ContentType for RecipeContent
    recipe_content_type = ContentType.objects.get_for_model(RecipeContent)

    # Access the ProductItem through the product's product_items relation
    product_item = product.product_items.first()

    assert product.product_items.count() == 1
    assert product_item.content_type == recipe_content_type
    assert product_item.content_object == recipe_content

@pytest.mark.unit
@pytest.mark.system
@pytest.mark.integration
@pytest.mark.django_db
def test_product_admin_list_view(client, admin_user):
    client.force_login(admin_user)
    url = reverse('admin:products_product_changelist')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.unit
@pytest.mark.system
@pytest.mark.integration
@pytest.mark.django_db
def test_product_admin_change_view(client, admin_user, product):
    client.force_login(admin_user)
    url = reverse('admin:products_product_change', args=(product.id,))
    response = client.get(url)
    assert response.status_code == 200