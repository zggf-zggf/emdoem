from django.forms import ModelForm
from django import forms
from base.models import Problem

class UploadForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'category',]