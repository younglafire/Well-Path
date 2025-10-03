from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Comment, Like
# Create your views here.

@login_required
@require_POST
def like_goal(request, goal_id):
    from .models import Goal # Import here to avoid circular import issues
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

    # fresh count
    likes_count = goal.likes_count

    return JsonResponse({
        "liked": liked,
        "likes_count": likes_count
    })

@login_required
def comment_goal(request, goal_id):
    from goals.models import Goal  # Import here to avoid circular import issues
    goal = get_object_or_404(Goal, id=goal_id)

    if request.method == "POST":
        import json
        data = json.loads(request.body)
        text = data.get("text", "").strip()
        
        if text:
            comment = Comment.objects.create(user=request.user, goal=goal, text=text)
            return JsonResponse({
                "success": True,
                "id": comment.id,
                "user": comment.user.username,
                "text": comment.text,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            })
        else:
            return JsonResponse({"error": "Comment text is required"}, status=400)

    elif request.method == "GET":
        # Get comments
        comments = []
        for comment in goal.comments.order_by("created_at"):
            comments.append({
                "id": comment.id,
                "user": comment.user.username,
                "text": comment.text,
                "created_at": comment.created_at.isoformat(),
            })
        return JsonResponse(list(comments), safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)
