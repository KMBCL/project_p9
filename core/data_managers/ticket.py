"""Services and configurations for creating, reading, updating and deleting tickets."""

from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING, Any

from core.models.ticket import Ticket

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from core.models.user import User


@dataclass
class TicketCreateConfig:
    """Input data for creating a ticket."""

    title: str
    description: str
    image: bytes
    request_user: User


@dataclass
class TicketCollectionConfig:
    """Input data for listing a user's tickets."""

    request_user: User


@dataclass
class TicketDetailConfig:
    """Input data for retrieving a single ticket."""

    request_user: User
    pk: int


@dataclass
class TicketUpdateConfig:
    """Input data for updating a ticket owned by a user."""

    request_user: User
    pk: int
    cleaned_data: dict[str, Any]


@dataclass
class TicketDeleteConfig:
    """Input data for deleting a ticket owned by a user."""

    request_user: User
    pk: int


class TicketService:
    """Handles creation, retrieval, update and deletion of tickets."""

    def __init__(self) -> None:
        pass

    def create_ticket(self, config: TicketCreateConfig) -> Ticket:
        """Create a ticket for the user."""
        ticket = Ticket.objects.create(
            title=config.title,
            description=config.description,
            user=config.request_user,
            image=config.image,
        )
        return ticket

    def get_tickets(self, config: TicketCollectionConfig) -> QuerySet[Ticket, Ticket]:
        """Return the tickets created by the user."""
        tickets = Ticket.objects.filter(user=config.request_user)
        return tickets

    def get_user_ticket(self, config: TicketDetailConfig) -> Ticket | None:
        """Return a ticket owned by the user, or None."""
        ticket = Ticket.objects.filter(
            user=config.request_user,
            pk=config.pk,
        ).first()
        return ticket

    def get_ticket(self, config: TicketDetailConfig) -> Ticket | None:
        """Return a ticket by its primary key, or None."""
        ticket = Ticket.objects.filter(pk=config.pk).first()
        return ticket

    def update_ticket(self, config: TicketUpdateConfig) -> Ticket | None:
        """Update a ticket owned by the user with the given data."""
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
        """Delete a ticket owned by the user."""
        detail_config = TicketDetailConfig(
            request_user=config.request_user,
            pk=config.pk,
        )
        ticket = self.get_user_ticket(detail_config)

        if ticket is None:
            return None

        ticket.delete()
