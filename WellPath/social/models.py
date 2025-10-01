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
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    goal = models.ForeignKey("goals.Goal", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # oldest first
        app_label = "social"

    def __str__(self):
        return f"{self.user} on {self.goal.title}: {self.text[:20]}"