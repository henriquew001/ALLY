from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser # Import CustomUser

def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            #before we save the user, we have to set the right username:
            username = form.cleaned_data.get("username")
            user = form.save(commit=False)
            user.username = username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CustomUserCreationForm()
    return render (request=request, template_name="accounts/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()  # Convert username to lowercase
            password = form.cleaned_data.get('password')
            
            # Find the user based on case-insensitive username
            try:
                user = CustomUser.objects.get(username__iexact=username)
                #if user exists, but the entered username is not the same as the user-username
                # -> set username correct for the authenticate process
                if user.username.lower() != username:
                  username = user.username
                user = authenticate(username=username, password=password)
                
            except CustomUser.DoesNotExist:
              user = None
            
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.username}.")  #Use the correct username
                return redirect("home:home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("home:home")
