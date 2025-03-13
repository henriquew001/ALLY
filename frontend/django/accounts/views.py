from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm  # Import LoginForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
              login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(
                request,
                _(f"Account created for {user.username}! You are now logged in."),
            )
            return redirect("home:home")
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST) # added this
        if form.is_valid(): # added this
            username = form.cleaned_data.get("username") # changed this
            password = form.cleaned_data.get("password") # changed this
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, _(f"You are now logged in as {user.username}."))
                return redirect("home:home")
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = LoginForm() # added this
    return render(request, "accounts/login.html", {"form": form})  # Pass the form

def user_logout(request):
    if request.user.is_authenticated:
        messages.success(request, _("You have successfully logged out."))
    logout(request)
    return redirect("home:home")
