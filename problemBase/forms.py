from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution


class UploadForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'category', 'problem_statement']


class SolutionForm(ModelForm):
    class Meta:
        model = Solution
        fields = ['content']