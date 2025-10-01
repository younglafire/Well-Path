from django.contrib import admin
from goals.models import User, Goal
from social.models import Like, Comment
from taxonomy.models import Category, Unit

# Register your models here.
admin.site.register(User)
admin.site.register(Goal)
admin.site.register(Like)
admin.site.register(Comment)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat', 'order')
    list_editable = ('order',)


