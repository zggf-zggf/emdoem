from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field
from .models import ProblemHistory

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



class EditProblemForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea)
    problem_instance = None
    old = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.problem_instance = kwargs['instance']
        self.old = {
            'name': self.problem_instance.name,
            'category': self.problem_instance.category,
            'source': self.problem_instance.source,
            'problem_statement': self.problem_instance.problem_statement
        }
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(Field('name', placeholder=NAME_PLACEHOLDER), 'category', css_class="col-lg-4"),
            Field('source', placeholder=SOURCE_PLACEHOLDER),
            'problem_statement',
            Field('comment', rows=2),
            Div(Submit('submit', 'Zapisz', css_class='d-flex'), css_class='d-flex flex-row justify-content-end'),
        )
        self.fields["problem_statement"].label = ""
        self.fields["name"].label = "Nazwa zadania"
        self.fields["category"].label = "Kategoria"
        self.fields["source"].label = "Źródło"
        self.fields["comment"].label = "Co zostało zmienione w zadaniu?"

    class Meta:
        model = Problem
        fields = ['name', 'category', 'source', 'problem_statement', 'comment']

    def save(self, **kwargs):
        if not ProblemHistory.objects.filter(problem=self.problem_instance).exists():
            ProblemHistory.objects.create(
                problem=self.problem_instance,
                name=self.old['name'],
                source=self.old['source'],
                problem_statement=self.old['problem_statement'],
                category=self.old['category'],
            )
        ProblemHistory.objects.create(
            problem=self.problem_instance,
            name=self.cleaned_data['name'],
            source=self.cleaned_data['source'],
            problem_statement=self.cleaned_data['problem_statement'],
            category=self.cleaned_data['category'],
            comment=self.cleaned_data['comment'],
        )
        instance = super().save(commit=False)
        instance.edited = True
        instance.save()
        return instance


