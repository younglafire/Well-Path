from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category, Unit
from django.http import JsonResponse
# Create your views here.
def category(request, category_slug):
    from .models import Goal  # Import Goal model here to avoid circular import issues

    category = get_object_or_404(Category, slug=category_slug)

    goals = Goal.objects.filter(
        user=request.user
    ).select_related(
        "category","unit"
    ).prefetch_related(
        "progresses"
    )

    active_goals = [g for g in goals if g.status == 'active']

    return render(request, "taxonomy/category.html", {
        "goals": active_goals,
        "category": category,
        "categories": Category.objects.all(),
    })


#Ajax view load units
def load_units(request):
    category_id = request.GET.get("category_id")
    units = Unit.objects.filter(categories__id=category_id).order_by("order")
    return JsonResponse(list(units.values("id", "name")), safe=False)

