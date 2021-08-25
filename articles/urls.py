from django.urls import path, include
from articles import views

urlpatterns = [
    path('', views.home , name='home'),
    path('articles/', views.article_search , name='article_search'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
]
