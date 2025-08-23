from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
# Create your views here.

def index(request):
    return render(request, "goals/index.html")

def feed(request):
    return render(request, "goals/feed.html")

def login_view(request):
    #Basically paste from django doc
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #to the main route
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "goals/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "goals/register.html", {"form": form})