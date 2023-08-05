from django.forms import ModelForm
from django import forms
from base.models import Problem, Solution, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div, Field
from .models import SolutionHistory

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

class EditSolutionForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea())
    solution_instance = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.solution_instance = kwargs['instance']
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('content', Field('comment', rows=2), css_class='form-group col-md-8 mb-0'), css_class='form-row'),
            Column(Div(Submit('submit', 'Zapisz', css_class='px-4'), css_class='justify-content-end d-flex flex-row px-4'), css_class='form-group col-md-8 mb-0')
        )
        self.fields["content"].label = ""
        self.fields["comment"].label = "Co zmieniło się w rozwiązaniu?"

    class Meta:
        model = Solution
        fields = ['content', 'comment']

    def save(self, **kwargs):
        if not SolutionHistory.objects.filter(solution=self.solution_instance).exists():
            SolutionHistory.objects.create(
                solution=self.solution_instance,
                content=self.solution_instance.content,
            )
        SolutionHistory.objects.create(
            solution=self.solution_instance,
            content=self.cleaned_data['content'],
            comment=self.cleaned_data['comment']
        )
        instance = super().save(commit=False)
        instance.edited = True
        instance.save()
        return instance