from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientForm


@login_required
def recipe_list(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {'recipes': qs}
    return render(request, 'recipes/list.html', context)


@login_required
def recipe_detail(request, id=None):
    context = {'recipe': get_object_or_404(Recipe, id=id, user=request.user)}
    return render(request, 'recipes/detail.html', context)

@login_required
def recipe_create(request):
    form = RecipeForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.save()
        return redirect(recipe.get_absolute_url())
    return render(request, 'recipes/create-update.html', context)

@login_required
def recipe_update(request, id=None):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=recipe)

    IngredientFormset = modelformset_factory(Ingredient, extra=2, form=IngredientForm)
    qs = recipe.ingredient_set.all()
    ingredient_formset = IngredientFormset(request.POST or None, queryset=qs)

    context = {'form': form, 'ingredient_formset': ingredient_formset, 'recipe': recipe}
    if all([form.is_valid(), ingredient_formset.is_valid()]):
        parent = form.save()
        for ingredient_form in ingredient_formset:
            child = ingredient_form.save(commit=False)
            if child.recipe is None:
                child.recipe = parent
            child.save()
        context['message'] = 'Your recipe was updated'
    return render(request, 'recipes/create-update.html', context)
