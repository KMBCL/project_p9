from typing import Any

from django import forms

from core.models.review import Review


class ReviewForm(forms.ModelForm[Review]):
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
        ]

        widgets: dict[str, Any] = {
            Review.headline.field.name: forms.TextInput(attrs={"class": "textinput"}),
            Review.rating.field.name: forms.TextInput(attrs={"class": "textinput"}),
            Review.body.field.name: forms.Textarea(attrs={"class": "textarea"}),
        }

        labels: dict[str, str] = {
            Review.headline.field.name: "Titre",
            Review.rating.field.name: "Note",
            Review.body.field.name: "Commentaire",
        }
