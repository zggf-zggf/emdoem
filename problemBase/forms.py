from django.forms import ModelForm
from django import forms
from base.models import Problem, Content


class UploadForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'category']

    image = forms.ImageField(required=False)
    content_text = forms.CharField(required=False)


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['content', 'image']
