from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now

from .models import Category, Goal, Progress,Unit
from .forms import CustomUserCreationForm, GoalForm, GoalEditForm
# Create your views here.

def index(request):
    return render(request, "goals/index.html")

def feed(request):
    goals = Goal.objects.filter(is_public=True, completed=False).order_by("-created_at")
    return render(request, "goals/feed.html", {"goals": goals})

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
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("dashboard", username=user.username)
            else:
                messages.error(request, "Authentication failed after registration.")
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
            return redirect("goal_detail", goal_id=goal.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = GoalForm()
    return render(request, "goals/create_goal.html", {"form": form})
def delete_goal(request, goal_id):
    if request.method == "POST":
        try:
            goal = Goal.objects.get(id=goal_id)
        except Goal.DoesNotExist:
            messages.error(request, "Goal not found.")
            return redirect("dashboard", username=request.user.username)
        # Only allow owner to delete
        if goal.user != request.user:
            messages.error(request, "You do not have permission to delete this goal.")
            return redirect("dashboard", username=request.user.username)
        goal.delete()
        messages.success(request, "Goal deleted successfully!")
        return redirect("dashboard", username=request.user.username)
    return redirect("dashboard", username=request.user.username)

#Ajax view load units
def load_units(request):
    category_id = request.GET.get("category_id")
    units = Unit.objects.filter(categories__id=category_id).order_by("order")
    return JsonResponse(list(units.values("id", "name")), safe=False)


def dashboard(request, username):
    goals = Goal.objects.filter(user__username=username, completed=False)
    return render(request, "goals/dashboard.html", {"username": username, "goals": goals})

def completed(request, username):
    goals = Goal.objects.filter(user__username=username, completed=True)
    return render(request, "goals/completed.html", {"username": username, "goals": goals})


def add_progress(request):
    if request.method == "POST":
        goal_id = request.POST.get("goal_id")
        value = float(request.POST.get("progress"))
        goal = Goal.objects.get(id=goal_id)

        today = now().date()
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            goal=goal,
            date=today,
            defaults={"value": value}
        )

        if not created:
            # Already exists → update instead of add new
            progress.value = value
            progress.save()

        messages.success(request, "Progress saved successfully!")

        # Check goal completion
        if goal.get_current_value() >= goal.target_value:
            goal.completed = True
            goal.finished_at = now()
            goal.save()
            messages.success(request, "Congratulations! You've achieved your goal.")

        return redirect("goal_detail", goal_id=goal_id)
    return redirect("index")

def goal_detail(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    today_progress = goal.has_today_progress(request.user)
    total_progress = goal.get_current_value()
    if goal.target_value > 0:
        progress_percent = min(100, (total_progress / goal.target_value) * 100)
    else:
        progress_percent = 0
    return render(request, "goals/goal_detail.html", {
        "goal": goal,
        "today_progress": today_progress,
        "total_progress": total_progress,
        "progress_percent": progress_percent,
    })

@login_required
def edit_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    if goal.user != request.user:
        messages.error(request, "You do not have permission to edit this goal.")
        return redirect("goal_detail", goal_id=goal.id)
    if request.method == "POST":
        form = GoalEditForm(request.POST, instance=goal)
        if form.is_valid():
            # Don't update category/unit even if POSTed
            goal = form.save(commit=False)
            goal.category = goal.category  # keep original
            goal.unit = goal.unit         # keep original
            goal.save()
            messages.success(request, "Goal updated successfully!")
            return redirect("goal_detail", goal_id=goal.id)
    else:
        form = GoalEditForm(instance=goal)
    return render(request, "goals/edit_goal.html", {"form": form, "goal": goal})

