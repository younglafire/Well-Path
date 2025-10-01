from django.db import models

# Create your models here.
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

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Categories"
        app_label = "taxonomy"

class Unit(models.Model):
    order = models.PositiveIntegerField(default=0)  
    name = models.CharField(max_length=20)  # km, kg, ml, days

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Units"
        app_label = "taxonomy"