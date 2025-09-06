from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class User(AbstractUser):
    pass

class Category(models.Model):
    order = models.PositiveIntegerField(default=0)  
    cat = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    units = models.ManyToManyField("Unit", blank=True, related_name="categories")

    def __str__(self):
        return self.cat

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        if not self.slug:
            base_slug = slugify(self.cat)
            slug = base_slug
            counter = 1

            # ensure unique slug
            while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("category", kwargs={"category_slug": self.slug})

    @property
    def active_goals_count(self):
        return sum(1 for goal in self.goals.filter(is_public=True) if goal.status == "active")

    class Meta:
        ordering = ["order"]


class Unit(models.Model):
    order = models.PositiveIntegerField(default=0)  
    name = models.CharField(max_length=20)  # km, kg, ml, days

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"


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
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def days_remaining(self):
        """Return number of days left until deadline (or None if no deadline)."""
        if self.deadline:
            delta = self.deadline - now().date()
            return delta.days
        return None

    def get_current_value(self):
        return sum(p.value for p in self.progresses.all())

    def has_today_progress(self, user):
        return self.progresses.filter(user=user, date=now().date()).first()

    # Derived logic
    def is_completed(self):
        return self.get_current_value() >= self.target_value

    def is_overdue(self):
        return self.deadline is not None and self.deadline < now().date() and not self.is_completed()

    @property
    def status(self):
        """Return a single status label: active / completed / overdue."""
        if self.is_completed():
            return "completed"
        elif self.is_overdue():
            return "overdue"
        return "active"
    
    def progress_percentage(self):
        total = self.get_current_value()
        if self.target_value == 0:
            return 0
        return min(100, (total / self.target_value) * 100)

    def __str__(self):
        return f"Goal: {self.title}, User: {self.user.username}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()




    

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="progresses")
    value = models.FloatField()
    date = models.DateField(default=now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'goal', 'date'], name='unique_daily_progress')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.goal.title} - {self.value} on {self.date}"
    
    # Test
    def is_today(self):
        return self.date == now().date()

class ProgressPhoto(models.Model):
    progress = models.ForeignKey("Progress", on_delete=models.CASCADE, related_name="photos")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def validate_image(image):
        max_size = 5 * 1024 * 1024  # 5 MB
        if image.size > max_size:
            raise ValidationError("Image file too large (max 5MB).")
        if not image.content_type.startswith("image/"):
            raise ValidationError("Invalid file type. Only images allowed.") 
    image = models.ImageField(upload_to="progress_photos/", validators=[validate_image])


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    goal = models.ForeignKey("Goal", on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "goal")  # one like per user per goal
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} liked {self.goal.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    goal = models.ForeignKey("Goal", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # oldest first

    def __str__(self):
        return f"{self.user} on {self.goal.title}: {self.text[:20]}"