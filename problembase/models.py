from django.db import models
from base.models import Problem, Category
from ckeditor.fields import RichTextField

# Create your models here.
class ProblemHistory(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    problem_statement = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

