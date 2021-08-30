from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Recipe, Ingredient, RecipeImage

User = get_user_model()

# admin.site.unregister(User)
#
# class RecipeInline(admin.StackedInline):
#     model = Recipe
#     extra = 0
#
#
# class UserAdmin(admin.ModelAdmin):
#     inlines = [RecipeInline]
#     list_display = ['username']
#
# admin.site.register(User, UserAdmin)


class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 0
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']

    # fields = ['name', 'quantity', 'unit', 'directions']


class IngredientAdmin(admin.ModelAdmin):
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
