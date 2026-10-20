from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING, Any

from core.models.ticket import Ticket

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from core.models.user import User


@dataclass
class TicketCreateConfig:
    title: str
    description: str
    image: bytes
    request_user: User


@dataclass
class TicketCollectionConfig:
    request_user: User


@dataclass
class TicketDetailConfig:
    request_user: User
    pk: int


@dataclass
class TicketUpdateConfig:
    request_user: User
    pk: int
    cleaned_data: dict[str, Any]


@dataclass
class TicketDeleteConfig:
    request_user: User
    pk: int


class TicketService:

    def __init__(self) -> None:
        pass

    def create_ticket(self, config: TicketCreateConfig) -> Ticket:
        ticket = Ticket.objects.create(
            title=config.title,
            description=config.description,
            user=config.request_user,
            image=config.image,
        )
        return ticket

    def get_tickets(self, config: TicketCollectionConfig) -> QuerySet[Ticket, Ticket]:
        tickets = Ticket.objects.filter(user=config.request_user)
        return tickets

    def get_user_ticket(self, config: TicketDetailConfig) -> Ticket | None:
        ticket = Ticket.objects.filter(
            user=config.request_user,
            pk=config.pk,
        ).first()
        return ticket

    def get_ticket(self, config: TicketDetailConfig) -> Ticket | None:
        ticket = Ticket.objects.filter(pk=config.pk).first()
        return ticket

    def update_ticket(self, config: TicketUpdateConfig) -> Ticket | None:
        detail_config = TicketDetailConfig(
            request_user=config.request_user,
            pk=config.pk,
        )
        ticket = self.get_user_ticket(detail_config)

        if ticket is None:
            return None

        for name, value in config.cleaned_data.items():
            setattr(ticket, name, value)
        ticket.save()

    def delete_ticket(self, config: TicketDeleteConfig) -> None:
        detail_config = TicketDetailConfig(
            request_user=config.request_user,
            pk=config.pk,
        )
        ticket = self.get_user_ticket(detail_config)

        if ticket is None:
            return None

        ticket.delete()
