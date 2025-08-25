from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path("feed/", views.feed, name="feed"),
    path('', views.index, name='index'),
    path('goals/', views.goals_view, name='goals'),
    path("create/", views.create_goal, name="create_goal"),
    path("ajax/load-units/", views.load_units, name="ajax_load_units"),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
]
