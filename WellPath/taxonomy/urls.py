from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('load-units/', views.load_units, name='load_units'),
]
