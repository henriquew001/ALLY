# recipes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientFormSet, RecipeIngredientForm
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredients.all()
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})

@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        if form.is_valid() and ingredient_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for ingredient_form in ingredient_formset:
                if ingredient_form.cleaned_data.get('name'):
                    ingredient_name = ingredient_form.cleaned_data['name']
                    try:
                        ingredient = Ingredient.objects.get(name=ingredient_name)
                    except Ingredient.DoesNotExist:
                        ingredient = Ingredient.objects.create(name=ingredient_name)
                    recipe.ingredients.add(ingredient, through_defaults={'quantity': request.POST.get(f"{ingredient_form.prefix}-quantity")})
            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'ingredient_formset': ingredient_formset})

@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        if form.is_valid() and ingredient_formset.is_valid():
            form.save()
            for ingredient_form in ingredient_formset:
                if ingredient_form.cleaned_data.get('name'):
                    ingredient_name = ingredient_form.cleaned_data['name']
                    try:
                        ingredient = Ingredient.objects.get(name=ingredient_name)
                    except Ingredient.DoesNotExist:
                        ingredient = Ingredient.objects.create(name=ingredient_name)
                    recipe.ingredients.add(ingredient, through_defaults={'quantity': request.POST.get(f"{ingredient_form.prefix}-quantity")})
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
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        ingredients = Ingredient.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse(list(ingredients), safe=False)
    return JsonResponse([], safe=False)
