# /home/heinrich/projects/ConsciousFit/frontend/cofi/ingredients/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Zentrale Definition der Einheiten
UNIT_CHOICES = [
    ('g', 'g'),
    ('ml', 'ml'),
    ('kg', 'kg'),
    ('l', 'l'),
]

class Allergen(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

class HouseholdMeasurement(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='g', verbose_name=_("Unit"))

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    reference_quantity = models.DecimalField(max_digits=6, decimal_places=2, default=100, verbose_name=_("Reference Quantity"))
    reference_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='g', verbose_name=_("Reference Unit"))
    kcal = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("kcal"))
    fat = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Fat"))
    protein = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Protein"))
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Carbohydrates"))
    sodium = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Sodium"))
    fiber = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Fiber"))
    # Vitamine
    vitamin_a = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin A"))
    vitamin_b1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B1"))
    vitamin_b2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B2"))
    vitamin_b3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B3"))
    vitamin_b5 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B5"))
    vitamin_b6 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B6"))
    vitamin_b7 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B7"))
    vitamin_b9 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B9"))
    vitamin_b12 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin B12"))
    vitamin_c = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin C"))
    vitamin_d = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin D"))
    vitamin_e = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin E"))
    vitamin_k = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Vitamin K"))
    allergens = models.ManyToManyField('Allergen', blank=True, verbose_name=_("Allergens"))
    not_recommended_for = models.ManyToManyField('Disease', related_name='not_recommended_ingredients', blank=True, verbose_name=_("Not Recommended For"))
    can_cause = models.ManyToManyField('Disease', related_name='causing_ingredients', blank=True, verbose_name=_("Can Cause"))
    # ... weitere Felder (Herkunft, etc.) ...

    def __str__(self):
        return self.name

class IngredientImage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='images', verbose_name=_("Ingredient"))
    image = models.ImageField(upload_to='ingredients/', verbose_name=_("Image"))

    def __str__(self):
        return f"{_('Image for')} {self.ingredient.name}"

class IngredientHouseholdMeasurement(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='household_measurements', verbose_name=_("Ingredient"))
    household_measurement = models.ForeignKey(HouseholdMeasurement, on_delete=models.CASCADE, verbose_name=_("Household Measurement"))
    quantity = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Quantity"))

    def __str__(self):
        return f"{self.quantity} {self.household_measurement.name} {_('of')} {self.ingredient.name}"

    def clean(self):
        if self.household_measurement.unit != self.ingredient.reference_unit:
            raise ValidationError(_("The unit of the household measurement must match the reference unit of the ingredient."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
