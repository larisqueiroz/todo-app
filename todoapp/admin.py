from django.contrib import admin
from .models import Task, Tag, Card

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'card', 'finished', 'created_at', 'updated_at', 'active')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at', 'updated_at', 'active')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'active')
    filter_vertical = ('tags',)