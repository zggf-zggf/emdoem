from django.db import models
from datetime import datetime, timedelta
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    pass


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
    source = models.CharField(max_length=100)

    def problem_id(self):
        return self.id

    def problem_name(self):
        return self.name

    def display(self):
        return self.problem_statement


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    upvote_counter = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    content = RichTextField(blank=True, null=True)
    # do usuniecia
    voters = models.JSONField("Voters", default={"voters": 1})

    def __str__(self):
        return str(self.id)

    def problem_id(self):
        return self.problem.id

    def problem_name(self):
        return self.problem.name

    def display(self):
        return self.content


class UserToProblem(models.Model):
    # CASCADE := when deleted, child will also be deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    surrendered = models.BooleanField(default=False)
    began_surrendering = models.BooleanField(default=False)
    surrender_end_time = models.DateTimeField(null=True)
    is_watching = models.BooleanField(default=False)
    last_visit = models.DateTimeField(null=True)

    def timestamp(self):
        self.last_visit = datetime.now()
        self.save()

    def start_surrendering(self):
        self.surrender_end_time = datetime.now() + timedelta(minutes=10)
        self.began_surrendering = True;
        self.save();

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    upvote_counter = models.IntegerField(default=0)

    def __str__(self):
        return str(self.content)

    def problem_id(self):
        return self.solution.problem.id

    def problem_name(self):
        return self.solution.problem.name

    def display(self):
        return self.content


class SolutionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + " " + str(self.solution) + " " + str(self.value)


class CommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + " " + str(self.comment) + " " + str(self.value)
