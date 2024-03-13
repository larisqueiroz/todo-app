from django.db import models
import uuid

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

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

class Card(Base):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'

    def __str__(self):
        return self.name

class Task(Base):
    description = models.CharField(max_length=255)
    card = models.ForeignKey(Card, related_name='tarefas', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
