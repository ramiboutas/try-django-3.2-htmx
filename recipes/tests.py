from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Recipe, Ingredient

User = get_user_model()


class RecipeTestCase(TestCase):
    def setUp(self):
        # user objects
        self.num_of_users = 1
        self.user_a = User.objects.create_user('cfe', password='whatever123')

        # recipe objects
        self.num_of_recipes = 3
        self.recipe_b = Recipe.objects.create(name='grilled chicken tacos',user=self.user_a)
        self.recipe_a = Recipe.objects.create(name='grilled chicken',user=self.user_a)
        self.recipe_c = Recipe.objects.create(name='tortilla',user=self.user_a)

        # ingredient objects
        self.num_of_ingredients = 2
        self.ingredient_a = Ingredient.objects.create(recipe = self.recipe_a, name='chicken', quantity='1/2', unit='pounds')
        self.ingredient_b = Ingredient.objects.create(recipe = self.recipe_a, name='chicken', quantity='NonSenseUnit', unit='pounds')

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), self.num_of_users)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), self.num_of_recipes)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = user.recipe_set.filter(user=user)
        self.assertEqual(qs.count(), self.num_of_recipes)

    def test_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.ingredient_set.all()
        self.assertEqual(qs.count(), self.num_of_ingredients)

    def test_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = Ingredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), self.num_of_ingredients)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = Ingredient.objects.filter(recipe__user = user)
        self.assertEqual(qs.count(), self.num_of_ingredients)

    def test_user_two_level_relation_reverse(self):
        # don't use this complicated method, there is a better way -> via recipes
        user = self.user_a
        ingredient_ids = list(user.recipe_set.all().values_list('ingredient__id', flat=True))
        qs = Ingredient.objects.filter(id__in=ingredient_ids)
        self.assertEqual(qs.count(), self.num_of_ingredients)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = Ingredient.objects.filter(recipe__id__in = ids)
        self.assertEqual(qs.count(), self.num_of_ingredients)

    def test_unit_validation_error(self):
        invalid_unit='nada'
        with self.assertRaises(ValidationError):
            ingredient = Ingredient(name='new', quantity=10, recipe=self.recipe_a, unit=invalid_unit)
            ingredient.full_clean() # this is similar to form.is_valid()

    def test_unit_validation_ok(self):
        valid_unit='gram'
        ingredient = Ingredient(name='new', quantity=10, recipe=self.recipe_a, unit=valid_unit)
        ingredient.full_clean() # this is similar to form.is_valid()

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.ingredient_a.quantity_as_float)
        self.assertIsNone(self.ingredient_b.quantity_as_float)
