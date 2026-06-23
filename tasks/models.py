from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="workers"
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        position_name = self.position.name if self.position else "No position"
        return f"{self.username}-{position_name}"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "A_URGENT", "Urgent"
        HIGH = "B_HIGH", "High"
        MEDIUM = "C_MEDIUM", "Medium"
        LOW = "D_LOW", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        Worker,
        blank=True,
        related_name="tasks"
    )

    class Meta:
        ordering = ["deadline", "priority"]

    def __str__(self):
        return self.name
