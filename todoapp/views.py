from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate

class TagAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            tags = Tag.objects.all().order_by('id').filter(active=True)

            paginator = PageNumberPagination()
            paged = paginator.paginate_queryset(tags, request)
            serializer = TagSerializer(paged, many=True)

            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.data.get('name') is None:
            return Response({"error": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            serializer = TagSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['username'] = request.user.username
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.data.get('id') is None:
            return Response({"error": "Identifier is required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            id = request.data.get('id')

            if id is None:
                return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                tag = Tag.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

            if request.data.get('name') is not None:
                tag.name = request.data.get('name')

            if request.data.get('color') is not None:
                tag.color = request.data.get('color')

            tag.updated_at = str(datetime.datetime.now())

            tag.save()

            serializer = TagSerializer(tag, many=False)

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class TagDetailView(APIView):
    def get(self, request, id):
        if id is None:
            return Response({"error": "Identifier is required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            try:
                tag = Tag.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        if id is None:
            return Response({"error": "Identifier is required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            try:
                tag = Tag.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

            tag.active = False
            tag.updated_at = str(datetime.datetime.now())

            tag.save()

            serializer = TagSerializer(tag)

            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class TaskAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.all().order_by('id').filter(active=True)

            paginator = PageNumberPagination()
            paged = paginator.paginate_queryset(tasks, request)
            serializer = TaskSerializer(paged, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.data.get('description') is None:
            return Response({"error": "Description required."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            card_id = request.data.get('card_id')
            card = Card.objects.filter(active=True).get(id=card_id)
            serializer = TaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['card_id'] = card.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            id = request.data.get('id')

            if id is None:
                return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                task = Task.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

            if request.data.get('description') is not None:
                task.description = request.data.get('description')

            if request.data.get('finished') is not None:
                task.finished = request.data.get('finished')

            task.updated_at = str(datetime.datetime.now())

            task.save()

            serializer = TaskSerializer(task, many=False)

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


class TaskDetailView(APIView):
    def get(self, request, id):
        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            try:
                task = Task.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            try:
                task = Task.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

            task.active = False
            task.updated_at = str(datetime.datetime.now())

            task.save()

            serializer = TaskSerializer(task)

            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class CardAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_authenticated:
                cards = Card.objects.all().order_by('id').filter(active=True)

                paginator = PageNumberPagination()
                paged = paginator.paginate_queryset(cards, request)
                serializer = CardSerializer(paged, many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.data.get('name') is None:
            return Response({"error": "Name required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            serializer = CardSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['user_id'] = request.user.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            id = request.data.get('id')

            if id is None:
                return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                card = Card.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

            if request.data.get('name') is not None:
                card.name = request.data.get('name')

            if request.data.get('tags') is not None:
                for item in request.data.get('tags'):
                    saved_item = Tag.objects.filter(active=True).get(id=item['id'])
                    card.tags.add(saved_item)

            if request.data.get('finished') is True:
                card.finished = request.data.get('finished')

            card.updated_at = str(datetime.datetime.now())

            card.save()

            serializer = CardSerializer(card, many=False)

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class CardDetailView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                card = Card.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CardSerializer(card)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        if id is None:
            return Response({"error": "Identifier required"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated:
            try:
                card = Card.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

            card.active = False
            card.updated_at = str(datetime.datetime.now())

            card.save()

            serializer = CardSerializer(card)

            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class CardTasksView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            if id is None:
                return Response({"error": "Identifier is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                card = Card.objects.filter(active=True).get(id=id)
            except:
                return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
            try:
                tasks = Task.objects.filter(active=True).filter(card_id=card.id)
                return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Error while getting data"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


class UserAPIView(APIView):
    def post(self, request):
        if request.data.get('username') or request.data.get('password') is None:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_superuser:
            try:
                serializer = UserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = User.objects.all().filter(username=request.data.get('username')).filter(is_active=True).first()
                if user is not None:
                    return Response({"erros": "user already exists."}, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.create_user(username=request.data.get('username'), password=request.data.get('password'))
                token = Token.objects.create(user=user)
                user.save()
                return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "Error while saving new user."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User not allowed."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        if request.user.is_superuser:
            try:
                users = User.objects.all().order_by('id').filter(is_active=True)
                paginator = PageNumberPagination()
                paged = paginator.paginate_queryset(users, request)
                serializer = UserSerializer(paged, many=True)
                return paginator.get_paginated_response(serializer.data)
            except:
                return Response({"error": "Error while getting data."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User not allowed."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            if request.data.get('id') is None:
                return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

            id = request.data.get('id')
            try:
                saved = User.objects.filter(is_active=True).get(id=id)
            except:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if request.data.get('email') is not None:
                saved.email = request.data.get('email')
                saved.save()
                user = User.objects.filter(is_active=True).filter(id=id).values('id', 'username', 'email', 'is_active').first()

                return Response(user, status.HTTP_200_OK)

        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailAPIView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                user = User.objects.filter(is_active=True).get(id=id)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                user = User.objects.filter(is_active=True).get(id=id)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            user.is_active = False
            user.updated_at = str(datetime.datetime.now())

            user.save()

            serializer = UserSerializer(user)

            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "User not allowed."}, status=status.HTTP_401_UNAUTHORIZED)

class UserCardsView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            if id is None:
                return Response({"error": "Identifier is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.filter(is_active=True).get(id=id)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            try:
                cards = Card.objects.filter(active=True).filter(user_id=id)
                return Response(CardSerializer(cards, many=True).data, status=status.HTTP_200_OK)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class UserTagsView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            if id is None:
                return Response({"error": "Identifier is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.filter(is_active=True).get(id=id)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            try:
                tags = Tag.objects.filter(active=True).filter(username=user.username)
                return Response(TagSerializer(tags, many=True).data, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Error while getting data"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogin(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            saved = User.objects.filter(is_active=True).get(username=request.data.get('username'))
            if saved is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            if not saved.check_password(request.data.get('password')):
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request=request, username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                try:
                    login(request=request, user=user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"username": request.data.get('username'), "token": token.key}, status=status.HTTP_200_OK)
                except ValueError as e:
                    return Response({"error": f"You have multiple authentication backends. {e}"}, status=status.HTTP_400_BAD_REQUEST)
                except TypeError as t:
                    return Response({"error": f"backend must be a dotted import path string. {t}"}, status=status.HTTP_400_BAD_REQUEST)
                except AttributeError as a:
                    return Response({"error": f"backend error. {a}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": f"Error while signing in. {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as t:
            return Response({"error": f"Error while signing in. {t}"}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as a:
            return Response({"error": f"Error while signing in. {a}"}, status=status.HTTP_400_BAD_REQUEST)