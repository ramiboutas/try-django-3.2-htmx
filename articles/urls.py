from django.urls import path, include
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.home , name='home'),
    path('articles/', views.article_search , name='search'),
    path('articles/create/', views.article_create, name='create'),
    path('articles/<slug:slug>/', views.article_detail, name='detail'),
]
