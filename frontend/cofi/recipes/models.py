# /home/heinrich/projects/ConsciousFit/frontend/cofi/recipes/models.py

from django.db import models
from django.utils.text import slugify
from ingredients.models import Ingredient

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    is_example = models.BooleanField(default=False)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    preparation_time = models.IntegerField(blank=True, null=True)
    cooking_time = models.IntegerField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class DishIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='dish_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)  # z.B. g, ml, Stück, TL, EL

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} in {self.recipe.title}"
