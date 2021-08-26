from django.contrib import admin

from .models import Recipe, Ingredient, RecipeImage

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    readonly_fields = ['user', 'timestamp', 'updated']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
