from django.db import models
from base.models import User
from datetime import datetime, timedelta

def content_default():
    return []

class Problemset(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.JSONField(default=content_default())
    date = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class UserToProblemset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problemset = models.ForeignKey(Problemset, on_delete=models.CASCADE)
    last_visit = models.DateTimeField(null=True)
    solved_count = models.IntegerField(default=0)
    surrendered_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=None, null=True)

    def timestamp(self):
        self.last_visit = datetime.now()
        self.save()

    def is_progress_valid(self):
        return self.total_count is not None

    def invalidate_progress_cache(self):
        self.total_count = None
        self.save()


class ProblemsetDuringEditing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problemset = models.ForeignKey(Problemset, null=True, on_delete=models.CASCADE)