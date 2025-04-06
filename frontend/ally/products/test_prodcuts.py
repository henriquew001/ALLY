import pytest
from django.urls import reverse
from django.test import Client
from products.models import ProductType, Product, RecipeBundle, VideoContent, DocumentContent, ProductItem
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
def test_product_recipe_relationship(product, recipe): # Annahme: product wird später noch verwendet?
    # 1. Erstelle das RecipeBundle zuerst (ohne 'recipe'-Argument)
    #    Gib ihm ggf. einen Namen zur Klarheit
    recipe_bundle = RecipeBundle.objects.create(name="Test Bundle für Beziehung") # Variable umbenannt

    # 2. Füge das Rezept zum ManyToManyField 'recipes' hinzu
    recipe_bundle.recipes.add(recipe)

    # 3. Überprüfe die Beziehung (wichtige Assertions hinzufügen!)
    assert recipe in recipe_bundle.recipes.all()
    assert recipe_bundle.recipes.count() == 1

    # --- Hier könnten weitere Tests folgen, die 'product' einbeziehen, ---
    # --- um dem Testnamen 'test_product_recipe_relationship' gerecht zu werden ---
    # --- z.B. Erstellen eines ProductItem, das product und recipe_bundle verknüpft ---
    # item = ProductItem.objects.create(product=product, content_object=recipe_bundle)
    # assert item.content_object == recipe_bundle
    # assert recipe_bundle in [pi.content_object for pi in product.product_items.all()]

    print(f"\nTested: RecipeBundle creation and adding Recipe via M2M - OK")

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