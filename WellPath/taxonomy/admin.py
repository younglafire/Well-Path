from django.contrib import admin
from .models import Category, Unit

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'category_count')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order', 'name')
    
    def category_count(self, obj):
        return obj.categories.count()
    category_count.short_description = 'Used in Categories'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat', 'order', 'slug', 'goal_count', 'unit_count')
    list_editable = ('order',)
    search_fields = ('cat', 'slug')
    prepopulated_fields = {'slug': ('cat',)}
    filter_horizontal = ('units',)  # Better UX for M2M
    ordering = ('order', 'cat')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('cat', 'slug', 'order')
        }),
        ('Associated Units', {
            'fields': ('units',),
            'description': 'Select which units are appropriate for this category'
        }),
    )
    
    def goal_count(self, obj):
        return obj.goals.count()
    goal_count.short_description = 'Goals'
    
    def unit_count(self, obj):
        return obj.units.count()
    unit_count.short_description = 'Units'