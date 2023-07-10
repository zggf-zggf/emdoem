from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Problem(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    problem_statement = RichTextField(blank=True, null=True)
    # SET_NULL := when deleted, this field will be null, therefore we will not lose the object.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    watchers = models.JSONField("Watchers", default={"watcher": "task"})


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    upvote_counter = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    content = RichTextField(blank=True, null=True)
    #do usuniecia
    voters = models.JSONField("Voters", default={"voters": 1})

    def __str__(self):
        return str(self.id)


class UserToProblem(models.Model):
    # CASCADE := when deleted, child will also be deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    surrendered = models.BooleanField(default=False)
    is_watching = models.BooleanField(default=False)
    last_visit = models.DateTimeField(null=True)

    def timestamp(self):
        self.last_visit = datetime.now()
        self.save()

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)

class SolutionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + " " + str(self.solution) + " " + str(self.value)
