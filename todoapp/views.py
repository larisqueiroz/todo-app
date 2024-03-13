from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tag, Task, Card
from .serializers import TaskSerializer, TagSerializer, CardSerializer

class TagAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class CardAPIView(APIView):
    def get(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
