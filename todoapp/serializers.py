from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'created_at', 'updated_at', 'active', 'username')

class CardSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ('id', 'name', 'created_at', 'updated_at', 'active', 'tags', 'user_id', 'finished')

class TaskSerializer(serializers.ModelSerializer):
    card = CardSerializer(many= False, read_only=True)

    class Meta:
        model = Task
        fields = (
            'id','description', 'card', 'finished', 'created_at', 'updated_at', 'active'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active')