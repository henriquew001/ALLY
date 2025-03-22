from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.models import Group  # Import the Group model

def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add the user to the "User" group
            user_group = Group.objects.get(name="User")  # Get the "User" group
            user.groups.add(user_group)  # Add the user to the group
            login(request, user)
            return redirect(reverse("home:home"))
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request=request, template_name="accounts/register.html", context={"register_form": form})
    else:
        form = CustomUserCreationForm()
    return render(request=request, template_name="accounts/register.html", context={"register_form": form})

def login_request(request):
    if request.user.is_authenticated:
        return redirect(reverse("home:home"))  # Weiterleitung, wenn der Benutzer eingeloggt ist

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # we still use the username field, but we get the email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)  # we changed the authenticate call to email=email and add the request
            if user is not None:
                login(request, user)
                return redirect(reverse("home:home"))  # add the reverse
            else:
                messages.error(request, "Invalid email or password.")  # changed the message
        else:
            messages.error(request, "Invalid email or password.")  # changed the message
    else:
        form = AuthenticationForm()  # add the else
    return render(request=request, template_name="accounts/login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    return redirect(reverse("home:home"))  # add the reverse
