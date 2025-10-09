from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:goal_id>/', views.like_goal, name='like_goal'),
]
