from django.shortcuts import render

app_name = 'home'

def home(request):
    return render(request, 'home/home.html')