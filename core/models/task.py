from django.db import models
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .user import User


class TaskStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    IN_PROGRESS = 'in_progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_users = models.ManyToManyField(User, through='TaskAssignment', related_name='tasks')

    class TaskTypes(models.TextChoices):
        MEETING = 'meeting', _('Meeting')
        ISSUE = 'issue', _('Issue')
        GOAL = 'goal', _('Goal')
        OTHER = 'other', _('Other')

    task_type = models.CharField(max_length=10, choices=TaskTypes, default=TaskTypes.OTHER)
    task_type_other = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    status = models.CharField(
        max_length=20,
        choices=TaskStatus,
        default=TaskStatus.PENDING
    )

    def update_status(self):
        """
        Compute task status dynamically:
        - If all `TaskAssignment` statuses are COMPLETED, the Task is COMPLETED.
        - If at least one is IN_PROGRESS, the Task is IN_PROGRESS.
        - Otherwise, the Task remains PENDING.
        """
        task_statuses = self.assignments.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status=TaskStatus.COMPLETED))
        )

        if task_statuses["total"] == 0:
            self.status = TaskStatus.PENDING  # No assignments exist yet
        elif task_statuses["total"] == task_statuses["completed"]:
            self.status = TaskStatus.COMPLETED
            self.completed_at = timezone.now()  # Mark as completed
        else:
            self.status = TaskStatus.IN_PROGRESS

        self.save(update_fields=['status', 'completed_at'])


class TaskAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    status = models.CharField(max_length=50, choices=TaskStatus, default=TaskStatus.PENDING)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.task.name} - {self.status}"

    def save(self, *args, **kwargs):
        """
        Automatically update Task completion time when all users complete their tasks.
        """
        super().save(*args, **kwargs)
        self.task.update_status()  # Automatically update task's status