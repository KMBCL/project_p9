"""Form confirming the deletion of an object."""

from typing import Any

from django import forms
from django.core.exceptions import ValidationError

CONFIRM = "CONFIRMER"


class DeleteForm(forms.Form):
    """Requires the user to type a confirmation word before deleting an object."""

    confirm = forms.CharField(
        label="Confirmation : Saisissez 'CONFIRMER' dans le champ",
        max_length=10,
        widget=forms.TextInput(attrs={"class": "textinput"}),
    )

    def clean(self) -> dict[str, Any] | None:
        """Check that the confirmation word was entered, case-insensitively."""
        cleaned_data = super().clean()
        if cleaned_data is None:
            raise ValidationError("Error to handle further")

        confirm: str = cleaned_data["confirm"]

        if confirm.upper() != CONFIRM:
            raise ValidationError("Veuillez saisir 'CONFIRMER' pour confirmer.")

        return cleaned_data
