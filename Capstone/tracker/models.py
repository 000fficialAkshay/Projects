from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    pass

class Course(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    name = models.CharField(max_length=100)
    resource_url = models.URLField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Part(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="parts"
    )
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Task(models.Model):
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    name = models.CharField(max_length=200)
    resource_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class DailyTask(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_tasks"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="daily_tasks"
    )
    date = models.DateField()
    planned_minutes = models.PositiveIntegerField()
    actual_seconds = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)