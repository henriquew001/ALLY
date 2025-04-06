from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientFormSet
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import transaction
from pymongo.errors import ConnectionFailure

@login_required
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredients.all()
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})

@login_required
@transaction.atomic
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        if form.is_valid() and ingredient_formset.is_valid():
            recipe = form.save(commit=False) # add commit=False
            recipe.author = request.user
            recipe.save()
            ingredient_formset.instance = recipe # set instance before saving
            ingredient_formset.save()
            return redirect('recipes:recipe_list')  # Redirect on success
        else:
            print("Form errors:")
            print(form.errors)
            print("Ingredient formset errors:")
            print(ingredient_formset.errors)
            # Render the template with errors - CORRECTED
            return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset, 'errors': form.errors, 'ingredient_errors': ingredient_formset.errors})
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset, 'errors': form.errors, 'ingredient_errors': ingredient_formset.errors})

@login_required
@transaction.atomic
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        if form.is_valid() and ingredient_formset.is_valid():
            recipe = form.save() # move form.save() here
            ingredient_formset.instance = recipe # set instance before saving
            ingredient_formset.save()
            return redirect('recipes:recipe_list')
        else:
            print("Form errors:")
            print(form.errors)
            print("Ingredient formset errors:")
            print(ingredient_formset.errors)
            # Render the template with errors - CORRECTED
            return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset, 'errors': form.errors, 'ingredient_errors': ingredient_formset.errors})
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset, 'errors': form.errors, 'ingredient_errors': ingredient_formset.errors})

@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        recipe.delete()
        return redirect('recipes:recipe_list')
    return render(request, 'recipes/recipe_delete.html', {'recipe': recipe})

def ingredient_autocomplete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        if settings.MONGO_CLIENT is not None:
            try:
                # Try to connect to MongoDB
                client = settings.MONGO_CLIENT
                client.admin.command('ping')  # Check connection
                db = client[settings.MONGO_DB_NAME]
                collection = db['ingredients']
                ingredients = collection.find({'name': {'$regex': query, '$options': 'i'}})
                results = [{'id': str(ingredient['_id']), 'name': ingredient['name']} for ingredient in ingredients]
                return JsonResponse(results, safe=False)
            except ConnectionFailure:
                # MongoDB not available, use placeholder
                results = [{'id': 'placeholder1', 'name': 'Placeholder Ingredient 1'},
                           {'id': 'placeholder2', 'name': 'Placeholder Ingredient 2'}]
                return JsonResponse(results, safe=False)
        else:
            results = [{'id': 'placeholder1', 'name': 'Placeholder Ingredient 1'},
                       {'id': 'placeholder2', 'name': 'Placeholder Ingredient 2'}]
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False) # Ensure a response is always returned


def debug_formset_view(request):
    # Überprüfe, ob die aktuelle Umgebung eine der erlaubten ist
    allowed_envs = ['dev', 'system', 'integration', 'unit', 'UAT']
    if settings.ENV not in allowed_envs:
        return HttpResponseForbidden("Debugging ist in dieser Umgebung nicht verfügbar.")

    # Wenn die Umgebung erlaubt ist, setze den Debugging-Workflow fort
    recipe = Recipe.objects.first() or Recipe.objects.create(
        name='Debug-Rezept',
        description='Nur zum Testen',
        instructions='Alles vermischen',
        prep_time=10,
        cook_time=15,
        servings=2,
    )

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe, prefix='form')

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe, prefix='form')

    return render(request, 'recipes/debug_formset.html', {
        'form': form,
        'formset': formset,
    })