from dataclasses import dataclass

from typing import Any

from django.db.models import QuerySet
from core.models.review import Review
from core.models.ticket import Ticket
from core.models.user import User


@dataclass
class ReviewCreateConfig:
    ticket_pk: int
    rating: int
    headline: str
    body: str
    request_user: User


@dataclass
class ReviewCollectionConfig:
    request_user: User


class ReviewService:

    def __init__(self):
        pass

    def create_review(self, config: ReviewCreateConfig):
        ticket = Ticket.objects.filter(pk=config.ticket_pk).first()
        if ticket is None:
            return None

        review = Review.objects.create(
            ticket=ticket,
            rating=config.rating,
            headline=config.headline,
            body=config.body,
            user=config.request_user,
        )
        return review

    def get_reviews(self, config: ReviewCollectionConfig):
        reviews = Review.objects.filter(user=config.request_user)
        return reviews
