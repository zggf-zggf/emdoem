from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field

class CommentForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "2", "cols": "80", "id": "comment-content", "maxlength": "300"}))
    solution_id = forms.IntegerField(widget=forms.HiddenInput(attrs={"value": "-1", "id": "comment-form-solution-id"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'solution_id',
            Div('content', css_class='d-flex w-100'),
            Div(Submit('submit-comment', 'Zapisz', css_class=''), css_class='d-flex flex-row justify-content-end px-2')
        )
        self.fields["content"].label = ""

    class Meta:
        model = Comment
        fields = ['content']
