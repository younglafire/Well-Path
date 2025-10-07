"""
Business logic for goals app.
Following HackSoft Django Style Guide principles.
"""

from django.utils.timezone import now
from django.db.models import QuerySet, Sum, Case, When, F, Q, Value, CharField, Count
from datetime import timedelta, date
from typing import Dict, List, Optional, Tuple

from .models import Goal, Progress, ProgressPhoto, User
from taxonomy.models import Category


# =============================================================================
# GOAL STATUS & CALCULATIONS (for single goals - when you already have the goal object)
# =============================================================================

def goal_is_completed(goal: Goal) -> bool:
    """
    Check if a goal has reached its target value.
    WARNING: This is for single goals. Use annotated queries for lists!
    """
    return goal.get_current_value() >= goal.target_value


def goal_is_overdue(goal: Goal) -> bool:
    """
    Check if a goal is past its deadline and not completed.
    WARNING: This is for single goals. Use annotated queries for lists!
    """
    if goal.deadline is None:
        return False
    return goal.deadline < now().date() and not goal_is_completed(goal)


def goal_get_status(goal: Goal) -> str:
    """
    Return goal status: 'completed', 'overdue', or 'active'.
    WARNING: This is for single goals. Use annotated queries for lists!
    """
    # First check if the goal has annotated values (from queryset)
    if hasattr(goal, 'current_value') and goal.current_value is not None:
        # Use the annotated value (fast!)
        if goal.current_value >= goal.target_value:
            return "completed"
        elif goal.deadline and goal.deadline < now().date():
            return "overdue"
        return "active"
    
    # Fallback to calculation (slow - only for single goals)
    if goal_is_completed(goal):
        return "completed"
    elif goal_is_overdue(goal):
        return "overdue"
    return "active"


def goal_progress_percentage(goal: Goal) -> float:
    """
    Calculate progress as a percentage (0-100).
    WARNING: This is for single goals. Use annotated queries for lists!
    """
    # Check if we have annotated value first
    if hasattr(goal, 'current_value') and goal.current_value is not None:
        total = goal.current_value or 0
    else:
        total = goal.get_current_value()
    
    if goal.target_value == 0:
        return 0
    return min(100, (total / goal.target_value) * 100)


# =============================================================================
# PROGRESS MANAGEMENT
# =============================================================================

def progress_create_or_update(
    *,
    user: User,
    goal: Goal,
    value: float,
    date: Optional[date] = None,
    images: Optional[List] = None
) -> Tuple[Progress, bool]:
    """
    Create or update daily progress for a goal.
    Returns (progress, created) tuple.
    
    Args:
        user: The user adding progress
        goal: The goal to track progress for
        value: Progress value to record
        date: Date of progress (defaults to today)
        images: List of image files to attach
    
    Returns:
        Tuple of (Progress instance, bool indicating if newly created)
    """
    if date is None:
        date = now().date()
    
    progress, created = Progress.objects.get_or_create(
        user=user,
        goal=goal,
        date=date,
        defaults={"value": value}
    )
    
    if not created:
        progress.value = value
        progress.save()
    
    # Handle image uploads
    if images:
        for img in images:
            ProgressPhoto.objects.create(progress=progress, image=img)
    
    return progress, created


def progress_check_goal_completion(goal: Goal) -> bool:
    """
    Check if goal just got completed and update finished_at timestamp.
    Returns True if goal was just marked as completed.
    """
    if goal_is_completed(goal) and goal.finished_at is None:
        goal.finished_at = now()
        goal.save(update_fields=['finished_at'])
        return True
    return False


# =============================================================================
# GOAL QUERIES & FILTERING (OPTIMIZED WITH ANNOTATE)
# =============================================================================

def goal_list_for_user(
    *,
    user: User,
    status_filter: Optional[str] = None
) -> List[Goal]:
    """
    Get all goals for a user, optionally filtered by status.
    Uses database aggregation for performance.
    
    Args:
        user: User to get goals for
        status_filter: Optional filter - 'active', 'completed', or 'overdue'
    
    Returns:
        List of Goal objects with annotated current_value and status
    """
    # ✅ Calculate current_value for ALL goals in ONE query
    goals = Goal.objects.filter(
        user=user
    ).select_related(
        'unit', 'category'
    ).prefetch_related(
        'progresses'
    ).annotate(
        # This calculates the sum in the database!
        current_value=Sum('progresses__value'),
        # This calculates status in the database!
        status=Case(
            When(current_value__gte=F('target_value'), then=Value('completed')),
            When(
                Q(deadline__lt=now().date()) & Q(current_value__lt=F('target_value')),
                then=Value('overdue')
            ),
            default=Value('active'),
            output_field=CharField()
        )
    )
    
    # ✅ Filter in the database, not in Python!
    if status_filter == "completed":
        goals = goals.filter(status='completed')
    elif status_filter == "overdue":
        goals = goals.filter(status='overdue')
    elif status_filter == "active":
        goals = goals.filter(status='active')
    
    return list(goals)


def goal_list_public(*, status_filter: str = "active") -> List[Goal]:
    """
    Get public goals for feed, filtered by status.
    Uses database aggregation for performance.
    """
    # Calculate in database
    goals = Goal.objects.filter(
        is_public=True
    ).select_related(
        'user', 'category', 'unit',
    ).prefetch_related(
        'likes', 'comments', 'progresses'
    ).annotate(
        current_value=Sum('progresses__value'),
        status=Case(
            When(current_value__gte=F('target_value'), then=Value('completed')),
            When(
                Q(deadline__lt=now().date()) & Q(current_value__lt=F('target_value')),
                then=Value('overdue')
            ),
            default=Value('active'),
            output_field=CharField()
        )
    )
    
    # Filter in database
    if status_filter == "active":
        goals = goals.filter(status='active')
    elif status_filter == "completed":
        goals = goals.filter(status='completed')
    elif status_filter == "overdue":
        goals = goals.filter(status='overdue')
    
    return list(goals)


# =============================================================================
# DASHBOARD STATISTICS (OPTIMIZED)
# =============================================================================

def dashboard_get_category_stats(user: User) -> Dict[int, Dict]:
    """
    Calculate statistics for each category for a user's dashboard.
    Uses database aggregation - NO Python loops!
    
    Returns:
        Dict mapping category_id to stats dict with keys:
        - category: Category object
        - active: count of active goals
        - completed: count of completed goals
        - total: total goals in category
    """
    # Calculate everything in the database!
    categories = Category.objects.annotate(
        # Count total goals for this user in this category
        total_goals=Count(
            'goals',
            filter=Q(goals__user=user),
            distinct=True
        ),
        # Count completed goals (finished_at is set)
        completed_goals=Count(
            'goals',
            filter=Q(goals__user=user, goals__finished_at__isnull=False),
            distinct=True
        ),
        # Count active goals (finished_at is null)
        active_goals=Count(
            'goals',
            filter=Q(goals__user=user, goals__finished_at__isnull=True),
            distinct=True
        )
    )
    
    # Convert to dict format
    category_stats = {}
    for category in categories:
        category_stats[category.id] = {
            'category': category,
            'active': category.active_goals,
            'completed': category.completed_goals,
            'total': category.total_goals
        }
    
    return category_stats


# =============================================================================
# CHART DATA GENERATION
# =============================================================================

def goal_get_chart_data(goal: Goal) -> Dict:
    """
    Generate chart data for goal detail page.
    Includes date range, values, cumulative progress, and averages.
    
    This is for a SINGLE goal, so it's OK to use get_current_value().
    """
    progress_history = goal.progresses.order_by("date")
    
    # Determine date range
    if progress_history.exists():
        start_date = progress_history.first().date
    else:
        start_date = goal.created_at.date()
    
    end_date = goal.deadline or now().date()
    
    # Build full date range
    all_dates = []
    current = start_date
    while current <= end_date:
        all_dates.append(current)
        current += timedelta(days=1)
    
    # Map progress by date
    progress_map = {p.date: p.value for p in progress_history}
    
    # Build aligned lists
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
            values.append(None)
            cumulative.append(None)
    
    # Calculate averages (using get_current_value is OK here - single goal)
    last_date = min(today, end_date)
    days_passed = (last_date - start_date).days + 1 if last_date >= start_date else 1
    
    total_progress = goal.get_current_value()
    avg_per_day = total_progress / days_passed if days_passed > 0 else 0
    
    # Calculate needed per day
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
    
    return {
        "dates": [d.strftime("%Y-%m-%d") for d in all_dates],
        "values": values,
        "cumulative": cumulative,
        "unit": goal.unit.name if goal.unit else "",
        "target": float(goal.target_value) if goal.target_value is not None else None,
        "avg_per_day": avg_per_day,
        "needed_per_day": needed_per_day,
    }