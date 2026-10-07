from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render, redirect


from core.template_path_creator import TemplatePathCreator

from core.forms.ticket import TicketForm
from core.data_managers.ticket import (
    TicketCreateConfig,
    TicketCollectionConfig,
    TicketDetailConfig,
    TicketUpdateConfig,
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
        config = TicketDetailConfig(
            request_user=request.user,
            request_parameter=request_parameters,
        )
        ticket_service = TickeService()
        ticket = ticket_service.get_ticket(config)

        return render(
            request=request,
            template_name=TemplatePathCreator.detail("ticket"),
            context={"ticket": ticket},
        )


class TicketUpdateView(View):
    def get(self, request: HttpRequest, request_parameters: str):
        config = TicketDetailConfig(
            request_user=request.user,
            request_parameter=request_parameters,
        )
        ticket_service = TickeService()
        ticket = ticket_service.get_ticket(config)
        form = TicketForm(instance=ticket)

        return render(
            request=request,
            template_name=TemplatePathCreator.update("ticket"),
            context={"form": form},
        )

    def post(self, request: HttpRequest, request_parameters: str):
        form = TicketForm(request.POST)
        if form.is_valid():
            config = TicketUpdateConfig(
                request_user=request.user, request_parameter=request_parameters, cleaned_data=form.cleaned_data
            )
            ticket_service = TickeService()
            ticket_service.update_ticket(config)
            return redirect("ticket_detail", request_parameters=request_parameters)


class TicketDeleteView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        pass
