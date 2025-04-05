from django.urls import path
from . import views

app_name = 'focoquiz'

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
]
