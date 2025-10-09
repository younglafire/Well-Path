from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Like
from goals.models import Goal  # Import from goals.models directly

@login_required
@require_POST
def like_goal(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    
    # check if user already liked
    like_obj = Like.objects.filter(user=request.user, goal=goal).first()
    
    if like_obj:
        # unlike
        like_obj.delete()
        liked = False
    else:
        # like
        Like.objects.create(user=request.user, goal=goal)
        liked = True
    
    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'likes_count': goal.likes.count()
    })

