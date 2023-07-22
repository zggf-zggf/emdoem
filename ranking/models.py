from django.db import models
from base.models import User, Problem

# Create your models here.
class ProblemSolvedLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " wbił zadanie " + str(self.problem)

