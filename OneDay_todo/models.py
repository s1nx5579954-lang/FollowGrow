from django.db import models

class OneDayList(models.Model):
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

    def __str__(self):
        return self.content

