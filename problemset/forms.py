from django.forms import ModelForm
from django import forms
from base.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field, HTML
from .models import Problemset

EXPLANATION = 'Zostaniesz przeniesionu do strony edycji, gdzie będziesz mógł dodać zadania do zbioru.'


class ProblemsetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(Field('name'), css_class="col-lg-8"),
            Field('description', rows=2),
            Div(HTML(EXPLANATION), css_class="d-flex mb-2"),
            Div(Submit('submit', 'Zapisz', css_class='d-flex'), css_class='d-flex flex-row justify-content-end'),
        )
        self.fields["name"].label = "Nazwa zbioru"
        self.fields["description"].label = "Opis (opcjonalny)"
        self.fields["description"].widget = forms.Textarea()


    class Meta:
        model = Problemset
        fields = ['name', 'description']


