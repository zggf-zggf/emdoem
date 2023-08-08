from django.db import models
from base.models import User

def content_default():
    return []

class Problemset(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.JSONField(default=content_default())

class ProblemsetDuringEditing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problemset = models.ForeignKey(Problemset, null=True, on_delete=models.CASCADE)