from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Content(models.Model):
    content = models.CharField(max_length=1000, null=True)
    image = models.ImageField(upload_to='base/iles/contents', null=True)

    def __str__(self):
        return str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Problem(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    # SET_NULL := when deleted, this field will be null, therefore we will not lose the object.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    watchers = models.JSONField("Watchers", default={"watcher": "task"})

    def __str__(self):
        return str(self.name)


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    upvote_counter = models.IntegerField()

    def __str__(self):
        return str(self.id)


class UserToProblem(models.Model):
    # CASCADE := when deleted, child will also be deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    surrendered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
