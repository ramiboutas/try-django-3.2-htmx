import pint

from django.db import models
from django.conf import settings
from django.urls import reverse

from .validators import validate_units
from .utils import number_str_to_float
"""
- Global:
    - Ingredients
    - Recipes
- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients

"""

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id':self.id})

    def get_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={'id':self.id})

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={'id':self.id})

    def get_ingredients(self):
        return self.ingredient_set.all()


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=20)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, validators=[validate_units])
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement #.to_base_units()

    def as_mks(self):
        # meters, kilograms, seconds
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        q = self.quantity
        float_q, success = number_str_to_float(q)
        if success:
            self.quantity_as_float = float_q
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
