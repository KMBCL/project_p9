from django import forms


class FollowingForm(forms.Form):
    username = forms.CharField(
        label="Nom utilisateur",
        max_length=100,
        widget=forms.TextInput,
    )
