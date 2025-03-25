from django.db import models
from .user import User

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=50)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    assigned_users = models.ManyToManyField(User, related_name='tasks')

    def __str__(self):
        return self.name