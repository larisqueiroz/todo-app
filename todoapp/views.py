from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tag, Task, Card
from .serializers import TaskSerializer, TagSerializer, CardSerializer
import datetime

class TagAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        tag = Tag.objects.get(id=id)

        if request.data['name'] is not None:
            tag.name = request.data['name']

        if request.data['color'] is not None:
            tag.color = request.data['color']

        tag.updated_at = str(datetime.datetime.now())

        tag.save()

        serializer = TagSerializer(tag, many=False)

        return Response(serializer.data, status.HTTP_200_OK)

class TagDetailView(APIView):
    def get(self, request, id):
        tag = Tag.objects.get(id=id)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status.HTTP_200_OK)

class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.get(id=id)

        if request.data['description'] is not None:
            task.description = request.data['description']

        task.updated_at = str(datetime.datetime.now())

        task.save()

        serializer = TaskSerializer(task, many=False)

        return Response(serializer.data, status.HTTP_200_OK)

class TaskDetailView(APIView):
    def get(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status.HTTP_200_OK)

class CardAPIView(APIView):
    def get(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        card = Card.objects.get(id=id)

        if request.data['name'] is not None:
            card.name = request.data['name']

        if request.data['tags'] is not None:
            for item in request.data['tags']:
                card.tags.add(item)

        card.updated_at = str(datetime.datetime.now())

        card.save()

        serializer = CardSerializer(card, many=False)

        return Response(serializer.data, status.HTTP_200_OK)

class CardDetailView(APIView):
    def get(self, request, id):
        card = Card.objects.get(id=id)
        serializer = CardSerializer(card)
        return Response(serializer.data, status.HTTP_200_OK)