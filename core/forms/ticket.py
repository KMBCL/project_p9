from typing import Any

from django import forms

from core.models.ticket import Ticket


class TicketForm(forms.ModelForm[Ticket]):
    field_order = [
        Ticket.title.field.name,
        Ticket.description.field.name,
        Ticket.image.field.name,
    ]

    class Meta:
        model = Ticket
        exclude = [
            Ticket.user.field.name,
            Ticket.time_created.field.name,
        ]

        widgets: dict[str, Any] = {
            Ticket.title.field.name: forms.TextInput(attrs={"class": "textinput"}),
            Ticket.description.field.name: forms.Textarea(attrs={"class": "textarea"}),
            Ticket.image.field.name: forms.FileInput(attrs={"class": "fileinput"}),
        }

        labels: dict[str, str] = {
            Ticket.title.field.name: "Titre",
            Ticket.description.field.name: "Description",
            Ticket.image.field.name: "Image",
        }
