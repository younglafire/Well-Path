from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from WellPath.goals.models import Category
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

def goals_view(request):

    return render(request, "goals/goals.html")

def create_goal(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        target_value = request.POST.get("target_value")
        unit = request.POST.get("unit")
        target_date = request.POST.get("target_date")

        # Basic validation
        if not title or not target_value or not unit:
            messages.error(request, "Title, Target Value, and Unit are required.")
            return redirect("create_goal")

        # Save the goal to the database (you'll need to implement this part)
        # For example:
        # Goal.objects.create(
        #     user=request.user,
        #     title=title,
        #     description=description,
        #     category=category,
        #     target_value=target_value,
        #     unit=unit,
        #     deadline=target_date
        # )
        messages.success(request, "Goal created successfully!")
        return redirect("goals")
    categories = Category.objects.all()
    return render(request, "goals/create_goal.html", {"categories": categories})
