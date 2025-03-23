# /home/heinrich/projects/ConsciousFit/frontend/cofi/ingredients/models.py

from django.db import models

class Allergen(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    reference_quantity = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    reference_unit = models.CharField(max_length=50, default='g')
    kcal = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    fat = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    protein = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sodium = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    fiber = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    # Vitamine
    vitamin_a = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b5 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b6 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b7 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b9 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_b12 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_c = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_d = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_e = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vitamin_k = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    allergens = models.ManyToManyField(Allergen, blank=True)
    not_recommended_for = models.ManyToManyField(Disease, related_name='not_recommended_ingredients', blank=True)
    can_cause = models.ManyToManyField(Disease, related_name='causing_ingredients', blank=True)
    # ... weitere Felder (Herkunft, etc.) ...

    def __str__(self):
        return self.name

class IngredientImage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ingredients/')

    def __str__(self):
        return f"Image for {self.ingredient.name}"
