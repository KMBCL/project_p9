from typing import Any

from django import forms

from core.models.review import Review


class ReviewForm(forms.ModelForm[Review]):
    class Meta:
        model = Review
        exclude = [
            Review.ticket.field.name,
            Review.user.field.name,
            Review.time_created.field.name,
        ]

        widgets: dict[str, Any] = {
            Review.rating.field.name: forms.TextInput(),
            Review.headline.field.name: forms.TextInput(),
            Review.body.field.name: forms.Textarea(),
        }
