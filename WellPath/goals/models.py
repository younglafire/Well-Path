from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Category(models.Model):
    order = models.PositiveIntegerField(default=0)  
    cat = models.CharField(max_length=64)
    units = models.ManyToManyField("Unit", blank=True, related_name="categories")

    def __str__(self):
        return self.cat

    class Meta:
        ordering = ['order']


class Unit(models.Model):
    order = models.PositiveIntegerField(default=0)  
    name = models.CharField(max_length=20)  # km, kg, ml, days

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="goals"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="goals"
    )
    target_value = models.FloatField()   
    current_value = models.FloatField(default=0)  
    deadline = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=[("ongoing", "Ongoing"), ("completed", "Completed")],
        default="ongoing"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percentage(self):
        if self.target_value > 0:
            return min(100, (self.current_value / self.target_value) * 100)
        return 0