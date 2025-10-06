from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Category, Unit
from goals.models import Goal  
@login_required
def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    # Filter goals for this category
    goals = Goal.objects.filter(
        user=request.user,
        category=category  # Add this filter!
    ).select_related(
        "category", "unit"
    ).prefetch_related(
        "progresses"
    )

    # Filter active goals using list comprehension
    active_goals = [g for g in goals if g.status == 'active']

    return render(request, "taxonomy/category.html", {
        "goals": active_goals,
        "category": category,
        "categories": Category.objects.all(),
    })

def load_units(request):
    """AJAX view to load units based on selected category."""
    category_id = request.GET.get("category_id")
    
    if not category_id:
        return JsonResponse([], safe=False)
    
    units = Unit.objects.filter(
        categories__id=category_id
    ).order_by("order").values("id", "name")
    
    return JsonResponse(list(units), safe=False)