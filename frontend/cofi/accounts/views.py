from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser  # Import CustomUser
from django.contrib.auth import get_user_model

def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Use email as username and make it lowercase
            email = form.cleaned_data.get("email")
            user = form.save(commit=False)
            user.username = email.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CustomUserCreationForm()
    return render(
        request=request,
        template_name="accounts/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username").lower()  # Treat the username field as email
            password = form.cleaned_data.get("password")

            # Find the user based on case-insensitive email
            try:
                user = CustomUser.objects.get(username__iexact=email)  # Changed to search by email
                user = authenticate(
                    username=user.username, password=password
                )

            except CustomUser.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                messages.info(
                    request, f"You are now logged in as {user.email}."
                )  # Use the email
                return redirect("home:home")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    form = AuthenticationForm()
    # change the username label for the login form
    form.fields["username"].label = "Email"
    return render(
        request=request, template_name="accounts/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home:home")
