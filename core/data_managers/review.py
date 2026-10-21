"""Services and configurations for creating, reading, updating and deleting reviews."""

from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING, Any

from django.db import transaction

from core.models.review import Review
from core.models.ticket import Ticket

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from core.models.user import User


@dataclass(kw_only=True)
class ReviewCreateConfig:
    """Input data for creating a ticket together with its review."""

    request_user: User
    ticket_title: str
    ticket_description: str
    ticket_image: bytes | None
    review_headline: str
    review_rating: int
    review_body: str


@dataclass
class ReviewCreateFromConfig:
    """Input data for creating a review in response to an existing ticket."""

    ticket_pk: int
    rating: int
    headline: str
    body: str
    request_user: User


@dataclass
class ReviewCollectionConfig:
    """Input data for listing a user's reviews."""

    request_user: User


@dataclass
class ReviewDetailConfig:
    """Input data for retrieving a single review owned by a user."""

    request_user: User
    pk: int


@dataclass
class ReviewUpdateConfig:
    """Input data for updating a review owned by a user."""

    request_user: User
    pk: int
    cleaned_data: dict[str, Any]


@dataclass
class ReviewDeleteConfig:
    """Input data for deleting a review owned by a user."""

    request_user: User
    pk: int


class ReviewValidator:
    """Checks business rules applying to reviews."""

    def has_user_reviews(self, request_user: User, ticket: Ticket) -> bool:
        """Return whether the user has already reviewed the ticket."""
        user_review_exists = Review.objects.filter(user=request_user, ticket=ticket).exists()
        return user_review_exists


class ReviewService:
    """Handles creation, retrieval, update and deletion of reviews."""

    def __init__(self) -> None:
        pass

    @transaction.atomic
    def create_review_and_ticket(self, config: ReviewCreateConfig) -> Review:
        """Create a ticket and its review atomically."""
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

    def create_review_from_ticket(self, config: ReviewCreateFromConfig) -> Review | None:
        """Create a review for an existing ticket, unless the user already reviewed it."""
        ticket = Ticket.objects.filter(pk=config.ticket_pk).first()
        if ticket is None:
            return None

        has_user_reviews = ReviewValidator().has_user_reviews(
            request_user=config.request_user,
            ticket=ticket,
        )

        if has_user_reviews:
            return None

        review = Review.objects.create(
            ticket=ticket,
            rating=config.rating,
            headline=config.headline,
            body=config.body,
            user=config.request_user,
        )
        return review

    def get_reviews(self, config: ReviewCollectionConfig) -> QuerySet[Review, Review]:
        """Return the reviews written by the user."""
        reviews = Review.objects.filter(user=config.request_user)
        return reviews

    def get_user_review(self, config: ReviewDetailConfig) -> Review | None:
        """Return a review owned by the user, or None."""
        review = (
            Review.objects.filter(
                user=config.request_user,
                pk=config.pk,
            )
            .select_related("user")
            .first()
        )
        return review

    def update_review(self, config: ReviewUpdateConfig) -> Review | None:
        """Update a review owned by the user with the given data."""
        review = Review.objects.filter(
            user=config.request_user,
            pk=config.pk,
        ).first()
        if review is None:
            return None

        for name, value in config.cleaned_data.items():
            setattr(review, name, value)
        review.save()

    def delete_review(self, config: ReviewDeleteConfig) -> None:
        """Delete a review owned by the user."""
        Review.objects.filter(
            user=config.request_user,
            pk=config.pk,
        ).delete()
