from rest_framework import serializers
from .models import Task, Card, Tag

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'description', 'card', 'finished', 'created_at', 'updated_at', 'active'
        )

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('name', 'created_at', 'updated_at', 'active')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'created_at', 'updated_at', 'active')