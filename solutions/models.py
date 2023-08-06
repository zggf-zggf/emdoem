from ckeditor.fields import RichTextField
from django.db import models

from base.models import Solution


class SolutionHistory(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = RichTextField(blank=True, null=True)
    comment = models.TextField(null=True)
