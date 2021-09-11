from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404
from django.urls import reverse

from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientForm


@login_required
def recipe_list(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {'recipes': qs}
    return render(request, 'recipes/list.html', context)


@login_required
def recipe_detail(request, id=None):
    recipe_hx_url = reverse('recipes:hx-detail', kwargs={'id': id})
    context = {'recipe_hx_url': recipe_hx_url}
    return render(request, 'recipes/detail.html', context)

@login_required
def hx_recipe_detail(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not Found")
    context = {'recipe': obj}
    return render(request, 'recipes/partials/detail.html', context)

@login_required
def recipe_create(request):
    form = RecipeForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.save()
        if request.htmx:
            headers = {"HX-Redirect": recipe.get_absolute_url()}
            return HttpResponse("created", headers=headers)
            # context = {'recipe': recipe}
            # headers = {"HX-Push": recipe.get_absolute_url()} #
            # return render(request, 'recipes/partials/detail.html', context)

    return render(request, 'recipes/create-update.html', context)

@login_required
def recipe_update(request, id=None):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=recipe)
    new_ingredient_url = reverse('recipes:hx-ingredient-create', kwargs={"parent_id": recipe.id})
    context = {'form': form, 'recipe': recipe, 'new_ingredient_url': new_ingredient_url}
    if form.is_valid():
        form.save()
        context['message'] = 'Your recipe was updated'

    if request.htmx:
        return render(request, 'recipes/partials/forms.html', context)
    return render(request, 'recipes/create-update.html', context)


@login_required
def hx_ingredient_update(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not Found")
    instance = None
    if id is not None:
        try:
            instance = Ingredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    form = IngredientForm(request.POST or None, instance=instance)
    url = instance.get_hx_edit_url() if instance else reverse('recipes:hx-ingredient-create', kwargs={"parent_id": parent_obj.id})
    context = {'ingredient': instance, 'form': form, 'url': url}
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['ingredient'] = new_obj
        return render(request, 'recipes/partials/ingredient-inline.html', context)
    return render(request, 'recipes/partials/ingredient-form.html', context)
