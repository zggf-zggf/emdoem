from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution
from django_quill.forms import QuillFormField


class UploadForm(ModelForm):
    #problem_statement = QuillFormField()
    class Meta:
        model = Problem
        fields = ['name', 'category', 'problem_statement']


class SolutionForm(ModelForm):
    #content = QuillFormField();
    class Meta:
        model = Solution
        fields = ['content']