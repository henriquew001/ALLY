from django.urls import path
from . import views

# app_name = 'home'  # This is the namespace

urlpatterns = [
    path("", views.home, name="home"),
    path('<str:lang>/', views.home, name='home_lang'),
]
