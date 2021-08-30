from django.urls import path
from .views import *


app_name = 'recipes'

urlpatterns = [
    path('', recipe_list, name='list'),
    path('create/', recipe_create, name='create'),
    path('<int:id>/edit/', recipe_update, name='update'),
    path('<int:id>/', recipe_detail, name='detail'),
]
