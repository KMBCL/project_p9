from typing import Any

from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nom utilisateur",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "textinput"},
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "textinput"},
        ),
    )
    confirmed_password = forms.CharField(
        label="Confirmer mot de passe",
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "textinput"},
        ),
    )

    def clean(self) -> dict[str, Any] | None:
        cleaned_data = super().clean()
        if cleaned_data is None:
            raise ValidationError("Error to handle further")
        password = cleaned_data.get("password")
        confirmed_password = cleaned_data.get("confirmed_password")

        if password != confirmed_password:
            raise ValidationError("Les mots de passe ne correspondent pas!")

        return cleaned_data
