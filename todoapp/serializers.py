from rest_framework import serializers
from .models import Task, Card, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'created_at', 'updated_at', 'active')

class CardSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    #tags = serializers.PrimaryKeyRelatedField(many= True, read_only=True)
    class Meta:
        model = Card
        fields = ('id', 'name', 'created_at', 'updated_at', 'active', 'tags')

class TaskSerializer(serializers.ModelSerializer):
    card = CardSerializer(many= False, read_only=True)

    #pk relanshinship
    #card = serializers.PrimaryKeyRelatedField(many= False, read_only=True)
    class Meta:
        model = Task
        fields = (
            'id','description', 'card', 'finished', 'created_at', 'updated_at', 'active'
        )