from dataclasses import dataclass

from typing import Any

from django.db.models import QuerySet, Exists
from core.models.review import Review
from core.models.ticket import Ticket
from core.models.user import User


@dataclass(kw_only=True)
class ReviewCreateConfig:
    request_user: User
    ticket_title: str
    ticket_description: str
    ticket_image: bytes | None
    review_headline: str
    review_rating: int
    review_body: str


@dataclass
class ReviewCreateFromConfig:
    ticket_pk: int
    rating: int
    headline: str
    body: str
    request_user: User


@dataclass
class ReviewCollectionConfig:
    request_user: User


@dataclass
class ReviewDetailConfig:
    request_user: User
    request_parameter: str


@dataclass
class ReviewUpdateConfig:
    request_user: User
    request_parameter: str
    cleaned_data: dict[str, Any]


@dataclass
class ReviewDeleteConfig:
    request_user: User
    request_parameter: str


class ReviewValidator:

    def has_user_reviews(self, request_user: User, ticket: Ticket) -> Exists:
        user_review_exists = Exists(Review.objects.filter(user=request_user, ticket=ticket))
        return user_review_exists


class ReviewService:

    def __init__(self):
        pass

    def create_review(self, config: ReviewCreateConfig):
        ticket = Ticket.objects.create(
            title=config.ticket_title,
            description=config.ticket_description,
            user=config.request_user,
            image=config.ticket_image,
        )
        review = Review.objects.create(
            ticket=ticket,
            rating=config.review_rating,
            headline=config.review_headline,
            body=config.review_body,
            user=config.request_user,
        )
        return review

    def create_from_review(self, config: ReviewCreateFromConfig):
        ticket = Ticket.objects.filter(pk=config.ticket_pk).first()
        if ticket is None:
            return None

        validator = ReviewValidator()
        if validator.has_user_reviews(
            request_user=config.request_user,
            ticket=ticket,
        ):
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

    def get_user_review(self, config: ReviewDetailConfig):
        review = (
            Review.objects.filter(
                user=config.request_user,
                pk=int(config.request_parameter),
            )
            .select_related()
            .first()
        )
        return review

    def update_review(self, config: ReviewUpdateConfig) -> Review | None:
        review = Review.objects.filter(
            user=config.request_user,
            pk=int(config.request_parameter),
        ).first()
        if review is None:
            return None

        for name, value in config.cleaned_data.items():
            setattr(review, name, value)
        review.save()

    def delete_review(self, config: ReviewDeleteConfig) -> None:
        review = Review.objects.filter(
            user=config.request_user,
            pk=int(config.request_parameter),
        ).first()

        if review is None:
            return None

        review.delete()
