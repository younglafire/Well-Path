from django.db import models
from django.conf import settings
# Create your models here.
class Like(models.Model):
    # Using settings.AUTH_USER_MODEL to avoid circular imports
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    goal = models.ForeignKey("goals.Goal", on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "goal")  # one like per user per goal
        ordering = ["-created_at"]
        app_label = "social"

    def __str__(self):
        return f"{self.user} liked {self.goal.title}"
    
