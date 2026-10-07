from dataclasses import dataclass
from core.models.ticket import Ticket
from core.models.user import User


@dataclass
class TicketInput:
    title: str
    description: str
    image: bytes
    request_user: User


class TickeService:

    def __init__(self) -> None:
        pass

    def create_ticket(self, ticket_input: TicketInput):
        ticket = Ticket.objects.create(
            title=ticket_input.title,
            description=ticket_input.description,
            user=ticket_input.request_user,
            image=ticket_input.image,
        )
        return ticket
