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
            if ingredient.reference_unit == dish_ingredient.unit:
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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='dish_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50, default='g')  # z.B. g, ml, Stück, TL, EL

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} in {self.recipe.title}"
