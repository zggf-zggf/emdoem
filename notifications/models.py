from django.db import models
from base.models import Comment, Solution, User, Problem
from django.urls import reverse

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=20)

class NewCommentNotification(Notification):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('solutions:solutions', kwargs={'pk': self.comment.solution.problem.id})

class NewSolutionNotification(Notification):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('solutions:solutions', kwargs={'pk': self.solution.problem.id})

class NewProblemNotification(Notification):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('problems:statement', kwargs={'pk': self.problem.id})
