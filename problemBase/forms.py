from django.forms import ModelForm
from django import forms
from base.models import Problem
from django_quill.forms import QuillFormField


class UploadForm(ModelForm):
    problem_statement = QuillFormField()
    class Meta:
        model = Problem
        fields = ['name', 'category']
