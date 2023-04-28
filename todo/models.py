from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    Priority = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True,)
    priority = models.IntegerField(choices=Priority, default="1")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    todo_list = models.ForeignKey(
        TodoList, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
