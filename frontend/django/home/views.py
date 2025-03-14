from django.shortcuts import render
from django.utils.translation import activate

def home(request, lang=None):
    if lang:
        activate(lang)
    return render(request, 'home.html')
