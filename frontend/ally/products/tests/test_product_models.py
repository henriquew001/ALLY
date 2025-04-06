# products/test_models.py

import pytest
from decimal import Decimal
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType

# Import models from the products app
from products.models import (
    ProductType,
    Product,
    RecipeBundle,
    VideoContent,
    DocumentContent,
    ProductItem
)

# Attempt to import Recipe from the recipes app
try:
    from recipes.models import Recipe
    Recipe_available = True
except ImportError:
    Recipe = None # Define Recipe as None if import fails
    Recipe_available = False
    print("\nWARNING: recipes.models.Recipe could not be imported. Tests needing Recipe will be skipped.")

# --- Fixtures for Reusable Test Data ---

@pytest.fixture
def product_type():
    """Provides a ProductType instance."""
    return ProductType.objects.create(name="Test Type", description="A type for testing")

@pytest.fixture
def product(product_type):
    """Provides a Product instance, requires product_type."""
    return Product.objects.create(
        title="Test Product",
        price=Decimal("99.99"),
        type=product_type,
        description="Test description"
    )

@pytest.fixture
def video_content():
    """Provides a VideoContent instance."""
    return VideoContent.objects.create(title="Test Video", video_url="http://example.com/test.mp4")

@pytest.fixture
def document_content():
    """Provides a DocumentContent instance."""
    # Note: FileField content is not tested here
    return DocumentContent.objects.create(title="Test Document")

# Fixtures for Recipes (only if Recipe model is available)
# We mark the fixtures themselves with django_db as they create objects
@pytest.fixture
def recipe_pasta():
    """Provides a Pasta Recipe instance."""
    if not Recipe_available: pytest.skip("Recipe model not available")
    return Recipe.objects.create(name="Pasta Test")

@pytest.fixture
def recipe_soup():
    """Provides a Soup Recipe instance with required fields."""
    if not Recipe_available: pytest.skip("Recipe model not available")
    # Beispielhafte Anpassung:
    return Recipe.objects.create(
        name="Soup Test",
        description="A test soup recipe.",
        instructions="Heat ingredients.",
        prep_time=10, # Erforderlich!
        cook_time=20, # Falls erforderlich
        servings=4    # Falls erforderlich
        # ... ggf. weitere Felder ...
    )

@pytest.fixture
def recipe_salad():
    """Provides a Salad Recipe instance with required fields."""
    if not Recipe_available: pytest.skip("Recipe model not available")
    # Beispielhafte Anpassung:
    return Recipe.objects.create(
        name="Salad Test",
        description="A test salad recipe.",
        instructions="Mix ingredients.",
        prep_time=15, # Erforderlich!
        cook_time=0,  # Salat hat oft keine Kochzeit
        servings=1    # Falls erforderlich
        # ... ggf. weitere Felder ...
    )

@pytest.fixture
def recipe_pasta():
    """Provides a Pasta Recipe instance with required fields."""
    if not Recipe_available: pytest.skip("Recipe model not available")
    # Fügen Sie hier Werte für ALLE benötigten Felder hinzu!
    # Die genauen Felder und Werte hängen von Ihrem Recipe-Modell ab.
    # Dies ist nur ein BEISPIEL:
    return Recipe.objects.create(
        name="Pasta Test",
        description="A test pasta recipe description.", # Falls benötigt und nicht blank=True
        instructions="1. Boil water. 2. Add pasta.", # Falls benötigt
        prep_time=5,  # Beispielwert für prep_time (z.B. in Minuten), DARF NICHT FEHLEN
        cook_time=10, # Beispielwert für cook_time (falls benötigt)
        servings=2,   # Beispielwert für servings (falls benötigt)
        # author=some_user_fixture, # Falls ein Autor benötigt wird (ForeignKey)
        # Fügen Sie weitere benötigte Felder hinzu...
    )


@pytest.fixture
def recipe_bundle_all():
    """Provides a RecipeBundle representing all recipes."""
    if not Recipe_available: pytest.skip("Recipe model not available")
    return RecipeBundle.objects.create(name="All Recipes Bundle", includes_all_recipes=True)

@pytest.fixture
def recipe_bundle_specific(recipe_pasta): # Takes recipe_pasta fixture as input
    """Provides a specific RecipeBundle instance (e.g., for Pasta)."""
    if not Recipe_available: pytest.skip("Recipe model not available")
    # Create a bundle named "Pasta Bundle"
    bundle = RecipeBundle.objects.create(
        name="Pasta Bundle",
        includes_all_recipes=False # It's specific, not all recipes
    )
    # Add the specific recipe(s) to it
    bundle.recipes.add(recipe_pasta)
    return bundle

# --- Test Functions ---

# Tests for ProductType
@pytest.mark.unit
@pytest.mark.django_db
def test_product_type_creation():
    """Test creating a ProductType instance."""
    pt = ProductType.objects.create(name="Book", description="Readable things")
    assert pt.name == "Book"
    assert pt.description == "Readable things"
    print("\nTested: ProductType Creation - OK")

@pytest.mark.unit
@pytest.mark.django_db
def test_product_type_str(product_type):
    """Test the __str__ method of ProductType."""
    assert str(product_type) == "Test Type"
    print("Tested: ProductType __str__ - OK")

@pytest.mark.unit
@pytest.mark.django_db
def test_product_type_unique_name(product_type):
    """Test that ProductType name is unique."""
    with pytest.raises(IntegrityError):
        ProductType.objects.create(name="Test Type") # Should fail, name exists
    print("Tested: ProductType Name Unique Constraint - OK")

# Tests for Product
@pytest.mark.unit
@pytest.mark.django_db
def test_product_creation(product_type):
    """Test creating a Product instance."""
    p = Product.objects.create(
        title="Another Product",
        price=Decimal("10.00"),
        type=product_type
    )
    assert p.title == "Another Product"
    assert p.price == Decimal("10.00")
    assert p.type == product_type
    print("Tested: Product Creation - OK")

@pytest.mark.unit
@pytest.mark.django_db
def test_product_str(product):
    """Test the __str__ method of Product."""
    assert str(product) == "Test Product"
    print("Tested: Product __str__ - OK")

# Tests for VideoContent
@pytest.mark.unit
@pytest.mark.django_db
def test_video_content_creation():
    """Test creating a VideoContent instance."""
    vc = VideoContent.objects.create(title="Intro Video", video_url="http://test.com/intro")
    assert vc.title == "Intro Video"
    assert vc.video_url == "http://test.com/intro"
    print("Tested: VideoContent Creation - OK")

@pytest.mark.unit
@pytest.mark.django_db
def test_video_content_str(video_content):
    """Test the __str__ method of VideoContent."""
    assert str(video_content) == "Video: Test Video"
    print("Tested: VideoContent __str__ - OK")

# Tests for DocumentContent
@pytest.mark.unit
@pytest.mark.django_db
def test_document_content_creation():
    """Test creating a DocumentContent instance."""
    dc = DocumentContent.objects.create(title="Manual PDF")
    assert dc.title == "Manual PDF"
    # assert dc.file is not None # Check default or how FileField behaves on create
    print("Tested: DocumentContent Creation - OK")

@pytest.mark.unit
@pytest.mark.django_db
def test_document_content_str(document_content):
    """Test the __str__ method of DocumentContent."""
    assert str(document_content) == "Document: Test Document"
    print("Tested: DocumentContent __str__ - OK")

# Tests for RecipeBundle (conditional on Recipe model)
@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_recipe_bundle_creation_specific(recipe_pasta, recipe_soup):
    """Test creating a RecipeBundle with specific recipes."""
    bundle = RecipeBundle.objects.create(name="Breakfast Bundle")
    bundle.recipes.add(recipe_pasta)
    assert bundle.name == "Breakfast Bundle"
    assert bundle.includes_all_recipes is False
    assert bundle.recipes.count() == 1
    assert recipe_pasta in bundle.recipes.all()
    assert recipe_soup not in bundle.recipes.all()
    print("Tested: RecipeBundle Specific Creation - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_recipe_bundle_creation_all():
    """Test creating a RecipeBundle representing all recipes."""
    bundle = RecipeBundle.objects.create(name="Complete Collection", includes_all_recipes=True)
    assert bundle.name == "Complete Collection"
    assert bundle.includes_all_recipes is True
    print("Tested: RecipeBundle All Recipes Creation - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_recipe_bundle_creation_no_name():
    """Test creating a RecipeBundle with name=None."""
    bundle = RecipeBundle.objects.create(name=None)
    assert bundle.name is None
    print("Tested: RecipeBundle No Name Creation - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_recipe_bundle_str_specific(recipe_bundle_specific):
    """Test RecipeBundle __str__ for specific recipes."""
    assert str(recipe_bundle_specific) == "Pasta Bundle"
    print("Tested: RecipeBundle __str__ (Specific) - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_recipe_bundle_str_all(recipe_bundle_all):
    """Test RecipeBundle __str__ for all recipes."""
    assert str(recipe_bundle_all) == "All Recipes Bundle (All Recipes)"
    print("Tested: RecipeBundle __str__ (All) - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_recipe_bundle_str_no_name():
    """Test RecipeBundle __str__ when name is None."""
    bundle = RecipeBundle.objects.create(name=None)
    assert str(bundle) == f"Unnamed Bundle (ID: {bundle.pk})"
    print("Tested: RecipeBundle __str__ (No Name) - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_get_effective_recipes_specific(recipe_pasta, recipe_soup):
    """Test get_effective_recipes for a specific bundle."""
    bundle = RecipeBundle.objects.create(name="Effective Test Bundle")
    bundle.recipes.add(recipe_soup)
    effective_recipes = bundle.get_effective_recipes()
    assert effective_recipes.count() == 1
    assert recipe_soup in effective_recipes
    assert recipe_pasta not in effective_recipes
    print("Tested: RecipeBundle get_effective_recipes (Specific) - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_get_effective_recipes_all(recipe_pasta, recipe_soup, recipe_salad):
    """Test get_effective_recipes for an 'all recipes' bundle."""
    bundle = RecipeBundle.objects.create(name="All Effective", includes_all_recipes=True)
    # Add one recipe - it should be ignored by get_effective_recipes
    bundle.recipes.add(recipe_pasta)

    effective_recipes = bundle.get_effective_recipes()
    all_recipe_count = Recipe.objects.count()

    assert effective_recipes.count() == all_recipe_count >= 3 # Check against total Recipes
    assert recipe_pasta in effective_recipes
    assert recipe_soup in effective_recipes
    assert recipe_salad in effective_recipes
    print("Tested: RecipeBundle get_effective_recipes (All) - OK")

# Tests for ProductItem (conditional on Recipe model for bundle test)
@pytest.mark.unit
@pytest.mark.django_db
def test_product_item_creation(product, video_content):
    """Test creating a ProductItem linking to VideoContent."""
    item = ProductItem.objects.create(
        product=product,
        content_object=video_content,
        order=5
    )
    assert item.product == product
    assert item.content_object == video_content
    assert item.content_type == ContentType.objects.get_for_model(VideoContent)
    assert item.object_id == video_content.pk
    assert item.order == 5
    print("Tested: ProductItem Creation (Video) - OK")

@pytest.mark.unit
@pytest.mark.django_db
def test_product_item_content_object_retrieval(product, document_content):
    """Test retrieving the object via content_object GenericForeignKey."""
    ProductItem.objects.create(product=product, content_object=document_content)
    item = ProductItem.objects.get(product=product, object_id=document_content.pk)
    assert item.content_object == document_content # Main check
    print("Tested: ProductItem content_object Retrieval (Document) - OK")

@pytest.mark.unit
@pytest.mark.skipif(not Recipe_available, reason="Recipe model not available")
@pytest.mark.django_db
def test_product_item_content_object_bundle(product, recipe_bundle_specific):
    """Test GenericForeignKey linking to a RecipeBundle."""
    ProductItem.objects.create(product=product, content_object=recipe_bundle_specific)
    item = ProductItem.objects.get(product=product, object_id=recipe_bundle_specific.pk)
    assert item.content_object == recipe_bundle_specific
    print("Tested: ProductItem content_object Retrieval (RecipeBundle) - OK")


@pytest.mark.unit
@pytest.mark.django_db
def test_product_item_ordering(product, video_content, document_content):
    """Test the default ordering of ProductItems for a product."""
    item1 = ProductItem.objects.create(product=product, content_object=video_content, order=2)
    item0 = ProductItem.objects.create(product=product, content_object=document_content, order=1)

    # Fetch items through the product's related manager
    items_for_product = product.product_items.all()

    # Meta.ordering is ['order'], so item0 (order=1) should come before item1 (order=2)
    assert list(items_for_product) == [item0, item1]
    print("Tested: ProductItem Ordering - OK")