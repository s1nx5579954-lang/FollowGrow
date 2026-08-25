# Monthly_todo/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MonthlyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def days_remaining(self):
        delta = self.deadline.date() - timezone.now().date()
        return delta.days


