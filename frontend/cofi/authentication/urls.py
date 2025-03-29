from django.urls import path, include
from django.contrib.auth.views import LogoutView

app_name = 'authentication'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
