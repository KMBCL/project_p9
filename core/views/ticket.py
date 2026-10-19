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
    TickeService,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from core.models.ticket import Ticket


def get_user_ticket(request: HttpRequest, request_parameters: str) -> Ticket | None:
    config = TicketDetailConfig(
        request_user=request.user,
        request_parameter=request_parameters,
    )
    ticket_service = TickeService()
    ticket = ticket_service.get_user_ticket(config)

    return ticket


class TicketCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = TicketForm()

        return render(
            request=request,
            template_name=TemplatePathCreator.create("ticket"),
            context={"form": form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
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
            ticket_service = TickeService()
            ticket_service.create_ticket(config)
            return redirect("feed")

        return render(
            request=request,
            template_name=TemplatePathCreator.create("ticket"),
            context={"form": form},
        )


class TicketUpdateView(View):

    def get(self, request: HttpRequest, request_parameters: str) -> HttpResponse:
        ticket = get_user_ticket(request, request_parameters)
        form = TicketForm(instance=ticket)

        return render(
            request=request,
            template_name=TemplatePathCreator.update("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str) -> HttpResponse:
        form = TicketForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            config = TicketUpdateConfig(
                request_user=request.user, request_parameter=request_parameters, cleaned_data=form.cleaned_data
            )
            ticket_service = TickeService()
            ticket_service.update_ticket(config)
            return redirect("user_posts")

        ticket = get_user_ticket(request, request_parameters)
        return render(
            request=request,
            template_name=TemplatePathCreator.update("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )


class TicketDeleteView(View):

    def get(self, request: HttpRequest, request_parameters: str) -> HttpResponse:
        form = DeleteForm()
        ticket = get_user_ticket(request, request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str) -> HttpResponse:
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = TicketDeleteConfig(
                request_user=request.user,
                request_parameter=request_parameters,
            )
            ticket_service = TickeService()
            ticket_service.delete_ticket(config)

            return redirect("user_posts")

        ticket = get_user_ticket(request, request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )
