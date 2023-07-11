from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CreateUser(UserCreationForm):
    password2 = None

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1']
