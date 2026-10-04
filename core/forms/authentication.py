from django import forms


class AuthenticationForm(forms.Form):
    username = forms.CharField(label="Nom utilisateur", max_length=100, widget=forms.TextInput)
    password = forms.CharField(label="Mot de passe", max_length=100, widget=forms.PasswordInput)
