from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Recipe, Ingredient

User = get_user_model()


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe', password='Qazxsw123')
        self.recipe_a = Recipe.objects.create(name='grilled chicken',user=self.user_a)
        self.recipe_b = Recipe.objects.create(name='grilled chicken tacos',user=self.user_a)
        self.ingredient_a = Ingredient.objects.create(recipe = self.recipe_a, name='chicken', quantity='1/2', unit='pounds')

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = user.recipe_set.filter(user=user)
        self.assertEqual(qs.count(), 2)

    def test_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.ingredient_set.all()
        self.assertEqual(qs.count(), 1)

    def test_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = Ingredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = Ingredient.objects.filter(recipe__user = user)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation_reverse(self):
        # don't use this complicated method, there is a better way -> via recipes
        user = self.user_a
        ingredient_ids = list(user.recipe_set.all().values_list('ingredient__id', flat=True))
        qs = Ingredient.objects.filter(id__in=ingredient_ids)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = Ingredient.objects.filter(recipe__id__in = ids)
        self.assertEqual(qs.count(), 1)
