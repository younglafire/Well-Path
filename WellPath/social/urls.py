from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:goal_id>/', views.like_goal, name='like_goal'),
    path('comment/<int:goal_id>/', views.comment_goal, name='comment_goal'),
]
