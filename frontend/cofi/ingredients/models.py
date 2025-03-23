# /home/heinrich/projects/ConsciousFit/frontend/cofi/ingredients/models.py

from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    kcal = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    fat = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    protein = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sugar = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    # ... weitere Nährwerte (Vitamine, Mineralien, etc.) ...
    allergens = models.TextField(blank=True, null=True)
    # ... weitere Felder (Herkunft, etc.) ...

    def __str__(self):
        return self.name
