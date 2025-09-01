from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path("feed/", views.feed, name="feed"),
    path('', views.index, name='index'),
    path('goals/', views.goals_view, name='goals'),
    path("edit/<int:goal_id>/", views.edit_goal, name="edit_goal"),
    path("create/", views.create_goal, name="create_goal"),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path("ajax/load-units/", views.load_units, name="ajax_load_units"),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('completed/<str:username>/', views.completed, name='completed'),
    path('goal/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('add_progress/', views.add_progress, name='add_progress'),  
    path('history/<int:goal_id>/', views.progress_history, name='progress_history'),
    path("api/goals", views.goals_api, name="goals_api"),

]
