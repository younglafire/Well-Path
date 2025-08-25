from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .models import Category,Unit
from .forms import CustomUserCreationForm, GoalForm
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

def goals_view(request):

    return render(request, "goals/goals.html")

def create_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Goal created successfully!")
            return redirect("index")  # Modify later
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()
    return render(request, "goals/create_goal.html", {"form": form})

#Ajax view load units
def load_units(request):
    category_id = request.GET.get("category_id")
    units = Unit.objects.filter(categories__id=category_id).order_by("order")
    return JsonResponse(list(units.values("id", "name")), safe=False)


def dashboard(request, username):
    return render(request, "goals/dashboard.html", {"username": username})