from django.db import models
from recipes.models import Recipe
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
 
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    contents = models.ManyToManyField(ContentType, through='ProductItem', related_name='products')

    def __str__(self):
        return self.title


class RecipeBundle(models.Model):
    name = models.CharField(
        "Bundle Name", # Display name in admin (optional but helpful)
        max_length=200,
        unique=False,
        null=True
    )
    description = models.TextField("Description", blank=True)
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name="Included Recipes", # Display name in admin
        blank=True, # Allow empty selection, especially if 'includes_all_recipes' is True
        help_text="Select specific recipes if 'Always include all recipes' is not checked."
    )
    includes_all_recipes = models.BooleanField(
        "Always include all recipes",
        default=False,
        help_text="If checked, this bundle represents all available recipes, regardless of the selection above."
    )

    def __str__(self):
        # Adjust __str__ to indicate when all recipes are included
        base_name = str(self.name) if self.name else f"Unnamed Bundle (ID: {self.pk})"
        if self.includes_all_recipes:
            return f"{base_name} (All Recipes)"
        return base_name

    def get_effective_recipes(self):
        """
        Returns the relevant queryset of recipes,
        based on the includes_all_recipes flag.
        """
        if self.includes_all_recipes:
            # Important: Import Recipe here or ensure it's available
            # in the module's global scope.
            from recipes.models import Recipe
            return Recipe.objects.all()
        else:
            return self.recipes.all()

    class Meta:
        verbose_name = "Recipe Bundle"
        verbose_name_plural = "Recipe Bundles"


class VideoContent(models.Model):  # Changed: Not abstract
    title = models.CharField(max_length=200)
    video_url = models.URLField()

    def __str__(self):
        return f"Video: {self.title}"

class DocumentContent(models.Model):  # Changed: Not abstract
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"Document: {self.title}"


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']