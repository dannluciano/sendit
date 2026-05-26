import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Nome",
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="Sobrenome",
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Obrigatório. Informe um e-mail valido.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class QuestionSearchForm(forms.Form):
    q = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Título ou enunciado",
                "class": "input",
                "type": "search",
            }
        ),
    )

    def clean_q(self):
        data = self.cleaned_data["q"]
        return re.sub(r"[^a-zA-Z0-9\s]", "", data)
