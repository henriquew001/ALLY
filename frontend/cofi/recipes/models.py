# /home/heinrich/projects/ConsciousFit/frontend/cofi/recipes/models.py

from django.db import models
from django.utils.text import slugify
from ingredients.models import Ingredient, HouseholdMeasurement
from django.utils.translation import gettext_lazy as _

class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_("Slug"))
    content = models.TextField(verbose_name=_("Content"))
    is_example = models.BooleanField(default=False, verbose_name=_("Is Example"))
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name=_("Image"))
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name=_("Preparation Time"))
    cooking_time = models.IntegerField(blank=True, null=True, verbose_name=_("Cooking Time"))
    servings = models.IntegerField(blank=True, null=True, verbose_name=_("Servings"))
    instructions = models.TextField(blank=True, null=True, verbose_name=_("Instructions"))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def calculate_nutritional_values(self):
        total_kcal = 0
        total_fat = 0
        total_protein = 0
        total_carbohydrates = 0
        total_sodium = 0
        total_fiber = 0
        total_vitamin_a = 0
        total_vitamin_b1 = 0
        total_vitamin_b2 = 0
        total_vitamin_b3 = 0
        total_vitamin_b5 = 0
        total_vitamin_b6 = 0
        total_vitamin_b7 = 0
        total_vitamin_b9 = 0
        total_vitamin_b12 = 0
        total_vitamin_c = 0
        total_vitamin_d = 0
        total_vitamin_e = 0
        total_vitamin_k = 0

        for dish_ingredient in self.dish_ingredients.all():
            ingredient = dish_ingredient.ingredient
            quantity = dish_ingredient.quantity

            # Umrechnungsfaktor berechnen
            if dish_ingredient.household_measurement:
                # Haushaltsmaß verwenden
                household_measurement = dish_ingredient.household_measurement
                try:
                    ingredient_household_measurement = ingredient.household_measurements.get(household_measurement=household_measurement)
                    conversion_factor = quantity * (ingredient_household_measurement.quantity / ingredient.reference_quantity)
                except Ingredient.household_measurements.RelatedObjectDoesNotExist:
                    conversion_factor = 0
            elif ingredient.reference_unit == dish_ingredient.unit:
                conversion_factor = quantity / ingredient.reference_quantity
            else:
                conversion_factor = 0 #TODO: Umrechnung von ml zu g

            total_kcal += (ingredient.kcal or 0) * conversion_factor
            total_fat += (ingredient.fat or 0) * conversion_factor
            total_protein += (ingredient.protein or 0) * conversion_factor
            total_carbohydrates += (ingredient.carbohydrates or 0) * conversion_factor
            total_sodium += (ingredient.sodium or 0) * conversion_factor
            total_fiber += (ingredient.fiber or 0) * conversion_factor
            total_vitamin_a += (ingredient.vitamin_a or 0) * conversion_factor
            total_vitamin_b1 += (ingredient.vitamin_b1 or 0) * conversion_factor
            total_vitamin_b2 += (ingredient.vitamin_b2 or 0) * conversion_factor
            total_vitamin_b3 += (ingredient.vitamin_b3 or 0) * conversion_factor
            total_vitamin_b5 += (ingredient.vitamin_b5 or 0) * conversion_factor
            total_vitamin_b6 += (ingredient.vitamin_b6 or 0) * conversion_factor
            total_vitamin_b7 += (ingredient.vitamin_b7 or 0) * conversion_factor
            total_vitamin_b9 += (ingredient.vitamin_b9 or 0) * conversion_factor
            total_vitamin_b12 += (ingredient.vitamin_b12 or 0) * conversion_factor
            total_vitamin_c += (ingredient.vitamin_c or 0) * conversion_factor
            total_vitamin_d += (ingredient.vitamin_d or 0) * conversion_factor
            total_vitamin_e += (ingredient.vitamin_e or 0) * conversion_factor
            total_vitamin_k += (ingredient.vitamin_k or 0) * conversion_factor

        return {
            'kcal': total_kcal,
            'fat': total_fat,
            'protein': total_protein,
            'carbohydrates': total_carbohydrates,
            'sodium': total_sodium,
            'fiber': total_fiber,
            'vitamin_a': total_vitamin_a,
            'vitamin_b1': total_vitamin_b1,
            'vitamin_b2': total_vitamin_b2,
            'vitamin_b3': total_vitamin_b3,
            'vitamin_b5': total_vitamin_b5,
            'vitamin_b6': total_vitamin_b6,
            'vitamin_b7': total_vitamin_b7,
            'vitamin_b9': total_vitamin_b9,
            'vitamin_b12': total_vitamin_b12,
            'vitamin_c': total_vitamin_c,
            'vitamin_d': total_vitamin_d,
            'vitamin_e': total_vitamin_e,
            'vitamin_k': total_vitamin_k,
        }

class DishIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='dish_ingredients', verbose_name=_("Recipe"))
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name=_("Ingredient"))
    quantity = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Quantity"))
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Unit"), editable=False)  # z.B. g, ml
    household_measurement = models.ForeignKey(HouseholdMeasurement, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Household Measurement"))

    def __str__(self):
        if self.household_measurement:
            return f"{self.quantity} {self.household_measurement.name} {self.ingredient.name} {_('in')} {self.recipe.title}"
        else:
            return f"{self.quantity} {self.unit} {self.ingredient.name} {_('in')} {self.recipe.title}"

    def save(self, *args, **kwargs):
        if self.household_measurement:
            self.unit = None
        else:
            self.unit = self.ingredient.reference_unit
        super().save(*args, **kwargs)
