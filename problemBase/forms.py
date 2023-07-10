from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution
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