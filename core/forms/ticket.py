from typing import Any

from django import forms

from core.models.ticket import Ticket


class TicketForm(forms.ModelForm[Ticket]):
    class Meta:
        model = Ticket
        exclude = [
            Ticket.user.field.name,
            Ticket.time_created.field.name,
        ]

        widgets: dict[str, Any] = {
            Ticket.title.field.name: forms.TextInput(),
            Ticket.description.field.name: forms.Textarea(),
            Ticket.image.field.name: forms.FileInput(),
        }
