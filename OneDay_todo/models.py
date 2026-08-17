from django.db import models
from django.contrib.auth.models import User


class OneDayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class OneDayTask(models.Model):
    one_day_list = models.ForeignKey(
        OneDayList,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    content = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.content

