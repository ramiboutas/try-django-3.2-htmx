from django.urls import path, include
from accounts import views

urlpatterns = [
    path('login/', views.user_login , name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
]
