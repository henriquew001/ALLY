# frontend/django/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required # add this line
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.utils.translation import gettext_lazy as _ # added for translation

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, _(f"You are now logged in as {username}.")) # translated
                return redirect("home:home")
            else:
                messages.error(request, _("Invalid username or password.")) # translated
        else:
            messages.error(request, _("Invalid username or password.")) # translated
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Only save the user if the form is valid.
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, _(f"Account created for {user.username}! You are now logged in.")) # translated
            return redirect("home:home")
        else:
            # The else block is executed only when the form is not valid
            # If there is an error, it will be displayed by the form.
            messages.error(request, _("Please correct the errors below."))  # translated
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, _("You have successfully logged out.")) # translated
    return redirect("home:home")
