from django.contrib.auth.decorators import login_required
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tag, Task, Card
from .serializers import TaskSerializer, TagSerializer, CardSerializer, UserSerializer
import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required

class TagAPIView(APIView):
    authentication_classes = [TokenAuthentication]  # Autenticação por token
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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

class UserAPIView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data['username']).filter(is_active=True)
            if user:
                return Response({"erros": "user already exists."}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
            token = Token.objects.create(user=user)
            user.save()
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        except:
            return Response({"error": "Error while saving new user."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        print(request.user)
        if request.user.is_authenticated:
            try:
                users = User.objects.all().filter(is_active=True)
                paginator = PageNumberPagination()
                paged = paginator.paginate_queryset(users, request)
                serializer = UserSerializer(paged, many=True)
                return paginator.get_paginated_response(serializer.data)
            except:
                return Response({"error": "Error while getting data."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogin(APIView):
    def post(self, request):
        try:
            saved = User.objects.filter(is_active=True).get(username=request.data['username'])
            print(request.data['username'])
            print(request.data['password'])
            #backend = 'django.contrib.auth.backends.ModelBackend'
            user = authenticate(request=request, username=request.data['username'], password=request.data['password'])
            print(user.backend)
            if user is not None:
                try:
                    login(request=request, user=user, backend=user.backend)
                    print(user.is_authenticated)
                    token, created = Token.objects.get_or_create(user=user)
                    #return Response({"username": request.data['username'], "token": token.key}, status=status.HTTP_200_OK)
                    return redirect('/api/v1/users/')
                except ValueError as e:
                    return Response({"error": f"You have multiple authentication backends. {e}"}, status=status.HTTP_400_BAD_REQUEST)
                except TypeError as t:
                    return Response({"error": f"backend must be a dotted import path string. {t}"}, status=status.HTTP_400_BAD_REQUEST)
                except AttributeError as a:
                    return Response({"error": f"backend error. {a}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                #return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
                return redirect('/api/v1/login/')
        except ValueError as e:
            return Response({"error": f"Error while signing in. {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as t:
            return Response({"error": f"Error while signing in. {t}"}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as a:
            return Response({"error": f"Error while signing in. {a}"}, status=status.HTTP_400_BAD_REQUEST)