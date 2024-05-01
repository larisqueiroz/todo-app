from django.db import models
import uuid
from django.contrib.auth.models import User

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Tag(Base):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10)
    username = models.CharField(max_length=20,default=None, blank=True, null=True,db_default=None)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Card(Base):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return self.name

class Task(Base):
    description = models.CharField(max_length=255)
    card = models.ForeignKey(Card, related_name='tasks', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'