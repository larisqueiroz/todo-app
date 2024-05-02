from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tag, Task, Card
from .serializers import *
import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
        if request.user.is_authenticated:
            serializer = TagSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['username'] = request.user.username
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

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
    def get(self, request):
        if request.user.is_authenticated:
            cards = Card.objects.all().order_by('id').filter(active=True)

            paginator = PageNumberPagination()
            paged = paginator.paginate_queryset(cards, request)
            serializer = CardSerializer(paged, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = CardSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['user_id'] = request.user.id
            print(request.data)
            card_saved = serializer.save()
            print(card_saved)
            print(type(card_saved))
            print(card_saved.id)
            if (len(request.data['tags']) > 0):
                for tag_id in request.data['tags']:
                    saved_tag = Tag.objects.get(id=tag_id['id'])
                    if saved_tag is not None and saved_tag.username == request.user.username:
                        card = Card.objects.get(id=card_saved.id)
                        card.tags.add(tag_id['id'])
                        card.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

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
            user = User.objects.all().filter(username=request.data['username']).filter(is_active=True).first()
            print(user)
            if user is not None:
                return Response({"erros": "user already exists."}, status=status.HTTP_400_BAD_REQUEST)
            print("2")
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
            print("3")
            token = Token.objects.create(user=user)
            user.save()
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        except:
            return Response({"error": "Error while saving new user."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        print(request.user)
        if request.user.is_authenticated:
            try:
                users = User.objects.all().order_by('id').filter(is_active=True)
                paginator = PageNumberPagination()
                paged = paginator.paginate_queryset(users, request)
                serializer = UserSerializer(paged, many=True)
                return paginator.get_paginated_response(serializer.data)
            except:
                return Response({"error": "Error while getting data."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            if request.data['id'] is None:
                return Response({"error": "Identifier required"}, status=status.HTTP_400_BAD_REQUEST)

            id = request.data['id']
            try:
                saved = User.objects.filter(is_active=True).get(id=id)
            except:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if request.data['email'] != saved.email:
                saved.email = request.data['email']
                saved.save()
                user = User.objects.filter(is_active=True).filter(id=id).values('id', 'username', 'email', 'is_active').first()
                print(type(user))

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
        if request.user.is_authenticated:
            try:
                print(id)
                user = User.objects.filter(is_active=True).get(id=id)
                print(user)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            user.is_active = False
            user.updated_at = str(datetime.datetime.now())

            user.save()

            serializer = UserSerializer(user)

            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogin(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            saved = User.objects.filter(is_active=True).get(username=request.data['username'])
            print(request.data['username'])
            print(request.data['password'])
            #backend = 'django.contrib.auth.backends.ModelBackend'
            if saved is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            if not saved.check_password(request.data['password']):
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request=request, username=request.data['username'], password=request.data['password'])
            print(user.backend)
            if user is not None:
                try:
                    login(request=request, user=user, backend=user.backend)
                    print(user.is_authenticated)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"username": request.data['username'], "token": token.key}, status=status.HTTP_200_OK)
                    #return redirect('/api/v1/users/')
                except ValueError as e:
                    return Response({"error": f"You have multiple authentication backends. {e}"}, status=status.HTTP_400_BAD_REQUEST)
                except TypeError as t:
                    return Response({"error": f"backend must be a dotted import path string. {t}"}, status=status.HTTP_400_BAD_REQUEST)
                except AttributeError as a:
                    return Response({"error": f"backend error. {a}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
                #return redirect('/api/v1/login/')
        except ValueError as e:
            return Response({"error": f"Error while signing in. {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError as t:
            return Response({"error": f"Error while signing in. {t}"}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as a:
            return Response({"error": f"Error while signing in. {a}"}, status=status.HTTP_400_BAD_REQUEST)