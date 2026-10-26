"""Model form used to create and update reviews."""

from typing import Any

from django import forms

from core.models.review import Review


class ReviewForm(forms.ModelForm[Review]):
    """Edits a review's headline, rating and body."""

    field_order = [
        Review.headline.field.name,
        Review.rating.field.name,
        Review.body.field.name,
    ]

    class Meta:
        model = Review
        exclude = [
            Review.ticket.field.name,
            Review.user.field.name,
            Review.time_created.field.name,
            # Review.rating.field.name,
        ]

        widgets: dict[str, Any] = {
            Review.headline.field.name: forms.TextInput(attrs={"class": "textinput"}),
            Review.body.field.name: forms.Textarea(attrs={"class": "textarea"}),
        }

        labels: dict[str, str] = {
            Review.headline.field.name: "Titre",
            Review.body.field.name: "Commentaire",
        }

    rating = forms.TypedChoiceField(
        choices=[(i, f" - {str(i)}") for i in range(6)],
        coerce=int,
        widget=forms.RadioSelect(attrs={"class": "form__radio"}),
        label="Note",
    )
