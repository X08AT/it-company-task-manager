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
        full_name = self.get_full_name()
        return f"{self.username} ({full_name})" if full_name else self.username


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.IntegerChoices):
        URGENT = 1, "Urgent"
        HIGH = 2, "High"
        MEDIUM = 3, "Medium"
        LOW = 4, "Low"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    assignees = models.ManyToManyField(
        Worker,
        blank=True,
        related_name="tasks"
    )

    class Meta:
        ordering = ["deadline", "priority", "name"]

    def __str__(self):
        return self.name
