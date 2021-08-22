from django.urls import path, include
from articles import views

urlpatterns = [
    path('', views.article_search , name='article_search'),
    path('create/', views.article_create, name='article_create'),
    path('<int:id>/', views.article_detail, name='article_detail'),
]
