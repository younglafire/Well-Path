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
        db_status=Case(
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
        goals = goals.filter(db_status='completed')
    elif status_filter == "overdue":
        goals = goals.filter(db_status='overdue')
    elif status_filter == "active":
        goals = goals.filter(db_status='active')
    
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
        'likes', 'progresses'
    ).annotate(
        current_value=Sum('progresses__value'),
        db_status=Case(
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
        goals = goals.filter(db_status='active')
    elif status_filter == "completed":
        goals = goals.filter(db_status='completed')
    elif status_filter == "overdue":
        goals = goals.filter(db_status='overdue')
    
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
    Intelligently groups data by days/weeks/months based on timespan.
    
    - Less than 60 days: Show daily data
    - 60-365 days: Group by weeks
    - More than 365 days: Group by months
    
    This is for a SINGLE goal, so it's OK to use get_current_value().
    """
    progress_history = goal.progresses.order_by("date")
    
    # Determine date range
    if progress_history.exists():
        start_date = progress_history.first().date
    else:
        start_date = goal.created_at.date()
    
    end_date = goal.deadline or now().date()
    today = now().date()
    
    # Calculate timespan to determine grouping strategy
    total_days = (end_date - start_date).days + 1
    
    # Map progress by date
    progress_map = {p.date: p.value for p in progress_history}
    
    if total_days <= 60:
        # Daily view for short goals
        chart_data = _generate_daily_chart_data(start_date, end_date, today, progress_map, goal)
    elif total_days <= 365:
        # Weekly view for medium-term goals
        chart_data = _generate_weekly_chart_data(start_date, end_date, today, progress_map, goal)
    else:
        # Monthly view for long-term goals
        chart_data = _generate_monthly_chart_data(start_date, end_date, today, progress_map, goal)
    
    # Calculate averages
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
    
    chart_data.update({
        "unit": goal.unit.name if goal.unit else "",
        "target": float(goal.target_value) if goal.target_value is not None else None,
        "avg_per_day": avg_per_day,
        "needed_per_day": needed_per_day,
    })
    
    return chart_data


def _generate_daily_chart_data(start_date: date, end_date: date, today: date, 
                                progress_map: Dict[date, float], goal: Goal) -> Dict:
    """Generate daily chart data for goals under 60 days."""
    all_dates = []
    current = start_date
    while current <= end_date:
        all_dates.append(current)
        current += timedelta(days=1)
    
    cumulative = []
    values = []
    running_total = 0.0
    
    for d in all_dates:
        if d <= today:
            v = float(progress_map.get(d, 0))
            values.append(v)
            running_total += v
            cumulative.append(running_total)
        else:
            values.append(None)
            cumulative.append(None)
    
    return {
        "dates": [d.strftime("%Y-%m-%d") for d in all_dates],
        "values": values,
        "cumulative": cumulative,
        "grouping": "daily"
    }


def _generate_weekly_chart_data(start_date: date, end_date: date, today: date,
                                 progress_map: Dict[date, float], goal: Goal) -> Dict:
    """Generate weekly chart data for goals 60-365 days."""
    # Find Monday of the week containing start_date
    week_start = start_date - timedelta(days=start_date.weekday())
    
    weeks = []
    labels = []
    cumulative = []
    values = []
    running_total = 0.0
    
    current_week_start = week_start
    while current_week_start <= end_date:
        current_week_end = min(current_week_start + timedelta(days=6), end_date)
        # Include weeks that have started (allow partial current week)
        if current_week_start <= today:
            # Sum up all progress in this week
            week_progress = 0.0
            day = max(current_week_start, start_date)
            while day <= min(current_week_end, today):
                week_progress += progress_map.get(day, 0)
                day += timedelta(days=1)

            values.append(week_progress)
            running_total += week_progress
            cumulative.append(running_total)
        else:
            values.append(None)
            cumulative.append(None)

        # Label format: "Week of Jan 1"
        label = f"{current_week_start.strftime('%b %d')}"
        labels.append(label)

        current_week_start += timedelta(days=7)
    
    return {
        "dates": labels,
        "values": values,
        "cumulative": cumulative,
        "grouping": "weekly"
    }


def _generate_monthly_chart_data(start_date: date, end_date: date, today: date,
                                  progress_map: Dict[date, float], goal: Goal) -> Dict:
    """Generate monthly chart data for goals over 365 days."""
    # Start from the first day of the month containing start_date
    month_start = date(start_date.year, start_date.month, 1)
    
    months = []
    labels = []
    cumulative = []
    values = []
    running_total = 0.0
    
    current_month = month_start
    while current_month <= end_date:
        # Calculate last day of this month
        if current_month.month == 12:
            next_month = date(current_month.year + 1, 1, 1)
        else:
            next_month = date(current_month.year, current_month.month + 1, 1)
        month_end = next_month - timedelta(days=1)
        month_end = min(month_end, end_date)
        # Include months that have started (allow partial current month)
        if current_month <= today:
            # Sum up all progress in this month
            month_progress = 0.0
            day = max(current_month, start_date)
            while day <= min(month_end, today):
                month_progress += progress_map.get(day, 0)
                day += timedelta(days=1)

            values.append(month_progress)
            running_total += month_progress
            cumulative.append(running_total)
        else:
            values.append(None)
            cumulative.append(None)

        # Label format: "Jan 2024"
        label = current_month.strftime("%b %Y")
        labels.append(label)

        # Move to next month
        if current_month.month == 12:
            current_month = date(current_month.year + 1, 1, 1)
        else:
            current_month = date(current_month.year, current_month.month + 1, 1)
    
    return {
        "dates": labels,
        "values": values,
        "cumulative": cumulative,
        "grouping": "monthly"
    }