from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div


class UploadForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'category', 'problem_statement']


class SolutionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('content', css_class='form-group col-md-8 mb-0'), css_class='form-row'),
            Column(Div(Submit('submit', 'Zapisz', css_class='px-4'), css_class='justify-content-end d-flex flex-row px-4'), css_class='form-group col-md-8 mb-0')
        )
        self.fields["content"].label = ""

    class Meta:
        model = Solution
        fields = ['content']

class CommentForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "2", "cols": "80", "id": "comment-content"}))
    solution_id = forms.IntegerField(widget=forms.HiddenInput(attrs={"value": "-1", "id": "comment-form-solution-id"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'solution_id',
            Div('content', css_class='d-flex w-100'),
            Div(Submit('submit', 'Zapisz', css_class=''), css_class='d-flex flex-row justify-content-end px-2')
        )
        self.fields["content"].label = ""

    class Meta:
        model = Comment
        fields = ['content']