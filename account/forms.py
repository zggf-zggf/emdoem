from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from base.models import User
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Div
from django import forms
from django.core.exceptions import ValidationError


class CreateUser(UserCreationForm):
    password2 = None
    email = forms.EmailField(required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('username', 'email', 'password1', css_class=""),
            Div(Submit('submit', 'Załóż konto', css_class='d-flex'), css_class='d-flex flex-row justify-content-end'),
        )
        self.fields["username"].label = "Nazwa użytkownika"
        self.fields["password1"].label = "Hasło"
        self.fields["email"].label = "Email"

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1']

    def save(self, commit=True):
        user = super(CreateUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Ten email jest już w użyciu.")
       return self.cleaned_data

class LoginUserForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika", max_length=100)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('username', 'password', css_class=""),
            Div(Submit('submit', 'Zaloguj', css_class='d-flex'), css_class='d-flex flex-row justify-content-end'),
        )

    class Meta:
        fields = ['username', 'password']
