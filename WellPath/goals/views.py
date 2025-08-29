from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta


from .models import Category, Goal, Progress,Unit
from .forms import CustomUserCreationForm, GoalForm, GoalEditForm
# Create your views here.

def index(request):
    return render(request, "goals/index.html")

def feed(request):
    goals = Goal.objects.filter(is_public=True, completed=False).order_by("-created_at")
    feed_goals = []
    today = now().date()
    for goal in goals:
        total_progress = goal.get_current_value()
        if goal.target_value > 0:
            progress_percent = min(100, (total_progress / goal.target_value) * 100)
        else:
            progress_percent = 0

        if goal.deadline and today <= goal.deadline:
            days_remaining = (goal.deadline - today).days + 1
        else:
            days_remaining = 0

        feed_goals.append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "unit": goal.unit,
            "target_value": goal.target_value,
            "deadline": goal.deadline,
            "days_remaining": days_remaining,
            "total_progress": total_progress,
            "progress_percent": progress_percent,
            "current_value": getattr(goal, "current_value", 0),
        })

    return render(request, "goals/feed.html", {"goals": feed_goals})

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
    dashboard_goals = []
    today = now().date()
    for goal in goals:
        total_progress = goal.get_current_value()
        if goal.target_value > 0:
            progress_percent = min(100, (total_progress / goal.target_value) * 100)
        else:
            progress_percent = 0

        # Days remaining calculation
        if goal.deadline and today <= goal.deadline:
            days_remaining = (goal.deadline - today).days + 1
        else:
            days_remaining = 0

        dashboard_goals.append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "unit": goal.unit,
            "target_value": goal.target_value,
            "deadline": goal.deadline,
            "days_remaining": days_remaining,
            "total_progress": total_progress,
            "progress_percent": progress_percent,
            "current_value": getattr(goal, "current_value", 0),  # fallback if needed
        })

    return render(request, "goals/dashboard.html", {
        "user": request.user,
        "goals": dashboard_goals,
    })

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

from datetime import timedelta

from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)

    progress_history = goal.progresses.order_by("date")
    today_progress = goal.has_today_progress(request.user)
    total_progress = goal.get_current_value()

    if goal.target_value > 0:
        progress_percent = min(100, (total_progress / goal.target_value) * 100)
    else:
        progress_percent = 0

    # --- Build full date range from first progress (or creation) to deadline ---
    if progress_history.exists():
        start_date = progress_history.first().date
    else:
        start_date = goal.created_at.date()

    end_date = goal.deadline or now().date()

    all_dates = []
    current = start_date
    while current <= end_date:
        all_dates.append(current)
        current += timedelta(days=1)

    # Map progress by date
    progress_map = {p.date: p.value for p in progress_history}

    # --- Build aligned lists ---
    cumulative = []
    values = []
    running_total = 0.0
    today = now().date()

    for d in all_dates:
        if d <= today:
            v = float(progress_map.get(d, 0))
            values.append(v)
            running_total += v
            cumulative.append(running_total)
        else:
            values.append(None)        # no data after today
            cumulative.append(None)    # line won't be drawn

    # --- Calculate averages ---
    # Days passed: from start_date to today (or deadline if earlier)
    start_date = all_dates[0]
    last_date = min(today, end_date)
    days_passed = (last_date - start_date).days + 1 if last_date >= start_date else 1

    total_progress = float(total_progress)
    avg_per_day = total_progress / days_passed if days_passed > 0 else 0

    # Needed per day to finish: (target - total_progress) / remaining days
    if goal.deadline and today <= goal.deadline:
        days_remaining = (goal.deadline - today).days + 1
    else:
        days_remaining = 0

    needed_per_day = 0
    if days_remaining > 0:
        needed_per_day = (goal.target_value - total_progress) / days_remaining
        needed_per_day = max(needed_per_day, 0)
    elif goal.target_value > total_progress:
        needed_per_day = goal.target_value - total_progress

    return render(request, "goals/goal_detail.html", {
        "goal": goal,
        "today_progress": today_progress,
        "total_progress": total_progress,
        "progress_percent": progress_percent,
        "progress_history": progress_history,
        "chart_data": {
            "dates": [d.strftime("%Y-%m-%d") for d in all_dates],
            "values": values,
            "cumulative": cumulative,
            "unit": goal.unit.name if goal.unit else "",
            "target": float(goal.target_value) if goal.target_value is not None else None,
            "avg_per_day": avg_per_day,
            "needed_per_day": needed_per_day,
        },
        "avg_per_day": avg_per_day,
        "needed_per_day": needed_per_day,
    })

@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
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

def progress_history(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    progress_history = Progress.objects.filter(goal=goal).order_by("-date")
    return render(request, "goals/history.html", {"goal": goal, "progress_history": progress_history})