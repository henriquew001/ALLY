from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.urls import reverse #add the import

def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #added this line to log in the user
            messages.success(request, "Registration successful." )
            return redirect(reverse("home:home")) #add the reverse
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.") #add the else
    else:
        form = CustomUserCreationForm() #add the else
    return render (request=request, template_name="accounts/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username') #we still use the username field, but we get the email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password) #we changed the authenticate call to email=email and add the request
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.") #changed the message
                return redirect(reverse("home:home")) #add the reverse
            else:
                messages.error(request,"Invalid email or password.") #changed the message
        else:
            messages.error(request,"Invalid email or password.") #changed the message
    else:
        form = AuthenticationForm() #add the else
    return render(request=request, template_name="accounts/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect(reverse("home:home")) #add the reverse
