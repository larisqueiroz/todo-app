"""
URL configuration for todoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('tags/', TagAPIView.as_view(), name='categories'),
    path('tags/<uuid:id>/', TagDetailView.as_view(), name='tag_by_id'),
    path('tasks/', TaskAPIView.as_view(), name='tasks'),
    path('tasks/<uuid:id>/', TaskDetailView.as_view(), name='task_by_id'),
    path('cards/', CardAPIView.as_view(), name='cards'),
    path('cards/<uuid:id>/', CardDetailView.as_view(), name='card_by_id'),
    path('admin/', admin.site.urls),
    path('users/', UserAPIView.as_view(), name='users'),
    path('login/', UserLogin.as_view(), name='login')
]
