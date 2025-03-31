from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    prep_time = models.IntegerField(help_text="Zubereitungszeit in Minuten")
    cook_time = models.IntegerField(help_text="Kochzeit in Minuten")
    servings = models.IntegerField(help_text="Anzahl der Portionen")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50, blank=True, null=True) # z.B. "1 Tasse", "200g"
    # Hier könnten wir später eine Verknüpfung zu OpenFoodFacts hinzufügen

    def __str__(self):
        return self.name
