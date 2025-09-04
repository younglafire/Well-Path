from django.contrib import admin
from .models import Category, User, Goal ,Unit,Like,Comment

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


