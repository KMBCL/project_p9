"""Form used to follow another user."""

from django import forms


class FollowingForm(forms.Form):
    """Collects the username of the user to follow."""

    username = forms.CharField(
        label="Nom utilisateur",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "textinput"}),
    )
