"""Views for creating, updating and deleting tickets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render, redirect


from core.template_path_creator import TemplatePathCreator

from core.forms.ticket import TicketForm
from core.forms.delete import DeleteForm
from core.data_managers.ticket import (
    TicketCreateConfig,
    TicketDetailConfig,
    TicketUpdateConfig,
    TicketDeleteConfig,
    TicketService,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from core.models.ticket import Ticket


def get_user_ticket(request: HttpRequest, pk: int) -> Ticket | None:
    """Return the ticket owned by the requesting user, or None."""
    config = TicketDetailConfig(
        request_user=request.user,
        pk=pk,
    )
    ticket_service = TicketService()
    ticket = ticket_service.get_user_ticket(config)

    return ticket


class TicketCreateView(View):
    """Creates a ticket requesting a review."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render an empty ticket form."""
        form = TicketForm()

        return render(
            request=request,
            template_name=TemplatePathCreator.create("ticket"),
            context={"form": form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """Create the ticket, or re-render the form with errors."""
        form = TicketForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            config = TicketCreateConfig(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"],
                request_user=request.user,
            )
            ticket_service = TicketService()
            ticket_service.create_ticket(config)
            return redirect("feed")

        return render(
            request=request,
            template_name=TemplatePathCreator.create("ticket"),
            context={"form": form},
        )


class TicketUpdateView(View):
    """Updates a ticket owned by the user."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render the ticket form pre-filled with the existing ticket."""
        ticket = get_user_ticket(request, pk)
        form = TicketForm(instance=ticket)

        return render(
            request=request,
            template_name=TemplatePathCreator.update("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Update the ticket, or re-render the form with errors."""
        form = TicketForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            config = TicketUpdateConfig(
                request_user=request.user, pk=pk, cleaned_data=form.cleaned_data
            )
            ticket_service = TicketService()
            ticket_service.update_ticket(config)
            return redirect("user_posts")

        ticket = get_user_ticket(request, pk)
        return render(
            request=request,
            template_name=TemplatePathCreator.update("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )


class TicketDeleteView(View):
    """Deletes a ticket owned by the user after confirmation."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render the deletion confirmation page."""
        form = DeleteForm()
        ticket = get_user_ticket(request, pk)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Delete the ticket, or re-render the confirmation page with errors."""
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = TicketDeleteConfig(
                request_user=request.user,
                pk=pk,
            )
            ticket_service = TicketService()
            ticket_service.delete_ticket(config)

            return redirect("user_posts")

        ticket = get_user_ticket(request, pk)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )
