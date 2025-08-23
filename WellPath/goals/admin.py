from django.contrib import admin
from .models import Category, User, Goal

# Register your models here.
admin.site.register(User)
admin.site.register(Goal)
admin.site.register(Category)

