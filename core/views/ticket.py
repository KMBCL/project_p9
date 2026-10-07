from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render, redirect


from core.template_path_creator import TemplatePathCreator

from core.forms.ticket import TicketForm
from core.data_managers.ticket import (
    TicketCreateConfig,
    TicketCollectionConfig,
    TickeService,
)

if TYPE_CHECKING:
    from django.http import HttpRequest


class TicketCreateView(View):
    def get(self, request: HttpRequest):
        form = TicketForm()

        return render(
            request=request,
            template_name=TemplatePathCreator.create("ticket"),
            context={"form": form},
        )

    def post(self, request: HttpRequest):
        form = TicketForm(request.POST)
        if form.is_valid():
            config = TicketCreateConfig(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"],
                request_user=request.user,
            )
            ticket_service = TickeService()
            ticket_service.create_ticket(config)
            return redirect("ticket_collection")


class TicketCollectionView(View):
    def get(self, request: HttpRequest):
        config = TicketCollectionConfig(request.user)
        ticket_service = TickeService()
        tickets = ticket_service.get_tickets(config)

        return render(
            request=request,
            template_name=TemplatePathCreator.collection("ticket"),
            context={"tickets": tickets},
        )


class TicketDetailView(View):
    def get(self, request: HttpRequest, request_parameters: str):
        pass


class TicketUpdateView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass


class TicketDeleteView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass
