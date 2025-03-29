from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
]
