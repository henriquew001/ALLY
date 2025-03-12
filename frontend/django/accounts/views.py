# frontend/django/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home:home") # Hier zu deiner Hauptseite weiterleiten
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}! You are now logged in.")
            print("Template Name:", 'accounts/register.html')
            return redirect("home:home") # Hier zu deiner Hauptseite weiterleiten
        else:
             for error in list(form.errors.values()):
                 messages.error(request, error)

    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_logout(request):
     logout(request)
     messages.info(request, "You have successfully logged out.")
     return redirect("home:home") # Hier zu deiner Hauptseite weiterleiten

# # Example for a home route
# def home(request):
#      return render(request, "home:home.html")
