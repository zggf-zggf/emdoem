from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field

NAME_PLACEHOLDER = 'MK Problemy rekurencyjne zad 24'
SOURCE_PLACEHOLDER = 'R.L.Graham, D.E.Knuth, O.Patashnik, Matematyka Konkretna, PWN, Warszawa 1996'


class UploadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(Field('name', placeholder=NAME_PLACEHOLDER), 'category', css_class="col-lg-4"),
            Field('source', placeholder=SOURCE_PLACEHOLDER),
            'problem_statement',
            Div(Submit('submit', 'Zapisz', css_class='d-flex'), css_class='d-flex flex-row justify-content-end'),
        )
        self.fields["problem_statement"].label = ""
        self.fields["name"].label = "Nazwa zadania"
        self.fields["category"].label = "Kategoria"
        self.fields["source"].label = "Źródło"


    class Meta:
        model = Problem
        fields = ['name', 'category', 'source', 'problem_statement']



class ProblemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(Field('name', placeholder=NAME_PLACEHOLDER), 'category', css_class="col-lg-4"),
            Field('source', placeholder=SOURCE_PLACEHOLDER),
            'problem_statement',
            Div(Submit('submit', 'Zapisz', css_class='d-flex'), css_class='d-flex flex-row justify-content-end'),
        )
        self.fields["problem_statement"].label = ""
        self.fields["name"].label = "Nazwa zadania"
        self.fields["category"].label = "Kategoria"
        self.fields["source"].label = "Źródło"

    class Meta:
        model = Problem
        fields = ['name', 'category', 'source', 'problem_statement']


