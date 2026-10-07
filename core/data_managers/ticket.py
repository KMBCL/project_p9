from dataclasses import dataclass
from core.models.ticket import Ticket
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


class TickeService:

    def __init__(self) -> None:
        pass

    def create_ticket(self, config: TicketCreateConfig):
        ticket = Ticket.objects.create(
            title=config.title,
            description=config.description,
            user=config.request_user,
            image=config.image,
        )
        return ticket

    def get_tickets(self, config: TicketCollectionConfig):
        tickets = Ticket.objects.filter(user=config.request_user)
        return tickets
