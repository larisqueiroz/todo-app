from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tag, Task, Card
from .serializers import TaskSerializer, TagSerializer, CardSerializer
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

class TagAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all().filter(active=True)

        paginator = PageNumberPagination()
        paged = paginator.paginate_queryset(tags, request)
        serializer = TagSerializer(paged, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tag = Tag.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            tag = Tag.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            tag = Tag.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

        tag.active = False
        tag.updated_at = str(datetime.datetime.now())

        tag.save()

        serializer = TagSerializer(tag)

        return Response(serializer.data, status.HTTP_204_NO_CONTENT)


class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all().filter(active=True)

        paginator = PageNumberPagination()
        paged = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paged, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.data['description'] is not None:
            task.description = request.data['description']

        task.updated_at = str(datetime.datetime.now())

        task.save()

        serializer = TaskSerializer(task, many=False)

        return Response(serializer.data, status.HTTP_200_OK)


class TaskDetailView(APIView):
    def get(self, request, id):
        try:
            task = Task.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            task = Task.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        task.active = False
        task.updated_at = str(datetime.datetime.now())

        task.save()

        serializer = TaskSerializer(task)

        return Response(serializer.data, status.HTTP_204_NO_CONTENT)


class CardAPIView(APIView):
    def get(self, request):
        cards = Card.objects.all().filter(active=True)

        paginator = PageNumberPagination()
        paged = paginator.paginate_queryset(cards, request)
        serializer = CardSerializer(paged, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            card = Card.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            card = Card.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CardSerializer(card)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            card = Card.objects.filter(active=True).get(id=id)
        except:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

        card.active = False
        card.updated_at = str(datetime.datetime.now())

        card.save()

        serializer = CardSerializer(card)

        return Response(serializer.data, status.HTTP_204_NO_CONTENT)
