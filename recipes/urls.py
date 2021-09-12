from django.urls import path
from .views import *


app_name = 'recipes'

urlpatterns = [
    path('', recipe_list, name='list'),
    path('create/', recipe_create, name='create'),
    path('<int:id>/edit/', recipe_update, name='update'),
    path('<int:id>/delete/', recipe_delete, name='delete'),
    path('<int:id>/', recipe_detail, name='detail'),
    path('hx/<int:id>/', hx_recipe_detail, name='hx-detail'),

    path('<int:id>/image-upload/', recipe_image_upload, name='image-upload'),

    path('hx/<int:parent_id>/ingredient/<int:id>/', hx_ingredient_update, name='hx-ingredient-detail'),

    path('<int:parent_id>/ingredient/<int:id>/delete/', ingredient_delete, name='ingredient-delete'),

    path('hx/<int:parent_id>/ingredient/new/', hx_ingredient_update, name='hx-ingredient-create'),


]
