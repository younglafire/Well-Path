from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    target_value = models.FloatField()   # ví dụ: 10 (km)
    current_value = models.FloatField(default=0)  # ví dụ: đã chạy 5 (km)
    unit = models.CharField(max_length=20)  # "km", "kg", "hours", v.v.
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