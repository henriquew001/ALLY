from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientFormSet
from django.conf import settings
from django.http import JsonResponse
import pymongo

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredient.objects.filter(recipe=recipe)

    ingredient_details = []
    if settings.MONGO_CONNECTION_SUCCESS:
        mongo_db = settings.MONGO_CLIENT[settings.MONGO_DB_NAME]
        food_collection = mongo_db["food"]

        for ingredient in ingredients:
            product = food_collection.find_one({"id": ingredient.openfoodfacts_id})
            if product:
                ingredient_details.append({
                    "name": product.get("product_name", "Unbekannt"),
                    "quantity": ingredient.quantity,
                })
            else:
                ingredient_details.append({
                    "name": "Produkt nicht gefunden",
                    "quantity": ingredient.quantity,
                })
    else:
        ingredient_details = [{"name": "MongoDB Verbindung fehlgeschlagen", "quantity": "N/A"}]

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'ingredients': ingredient_details})

def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        if form.is_valid() and ingredient_formset.is_valid():
            recipe = form.save()
            for ingredient_form in ingredient_formset:
                if ingredient_form.has_changed():
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    # Holen Sie sich die openfoodfacts_id aus dem POST-Daten
                    openfoodfacts_id = request.POST.get(f"{ingredient_form.prefix}-openfoodfacts_id")
                    ingredient.openfoodfacts_id = openfoodfacts_id
                    ingredient.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset})

def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        if form.is_valid() and ingredient_formset.is_valid():
            form.save()
            for ingredient_form in ingredient_formset:
                if ingredient_form.has_changed():
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    # Holen Sie sich die openfoodfacts_id aus dem POST-Daten
                    openfoodfacts_id = request.POST.get(f"{ingredient_form.prefix}-openfoodfacts_id")
                    ingredient.openfoodfacts_id = openfoodfacts_id
                    ingredient.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset})

def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_delete.html', {'recipe': recipe})

def ingredient_autocomplete(request):
    query = request.GET.get('query', '')
    results = []

    if settings.MONGO_CONNECTION_SUCCESS:
        mongo_db = settings.MONGO_CLIENT[settings.MONGO_DB_NAME]
        food_collection = mongo_db["food"]

        # Suche in der MongoDB nach Produkten, deren Name mit der Abfrage beginnt
        # Verwende einen regulären Ausdruck für eine case-insensitive Suche
        regex = f"^" + query  # Suche beginnt mit dem Query
        mongo_results = food_collection.find({"product_name": {"$regex": regex, "$options": "i"}}).limit(10) # Limit auf 10 Ergebnisse

        for result in mongo_results:
            results.append({
                "id": result.get("id"),  # Oder result.get("_id"), je nach deiner MongoDB
                "name": result.get("product_name", "Unbekannt"),
            })

    return JsonResponse(results, safe=False)