"""Service gathering the tickets and reviews posted by a user."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass


from django.db.models import Q, Exists, OuterRef, Value, BooleanField

from core.models.ticket import Ticket
from core.models.review import Review
from core.data_managers.helper.merge_posts import MergePostsConfig, merge_posts

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from core.models.user import User


@dataclass
class UserPostsConfig:
    """Input data for retrieving a user's own posts."""

    request_user: User


class UserPostsService:
    """Retrieves a user's own tickets and reviews and merges them into a single list."""

    def get_user_tickets(self, config: UserPostsConfig) -> QuerySet[Ticket, Ticket]:
        """Return the user's tickets, annotated as editable and with whether the user reviewed them."""
        user_reviews = Review.objects.filter(
            user=config.request_user,
            ticket=OuterRef("pk"),
        )
        tickets = Ticket.objects.filter(Q(user=config.request_user)).select_related()
        tickets = tickets.annotate(has_user_reviews=Exists(user_reviews))
        tickets = tickets.annotate(editable=Value(True, output_field=BooleanField()))
        return tickets

    def get_user_reviews(self, config: UserPostsConfig) -> QuerySet[Review, Review]:
        """Return the user's reviews, annotated as editable."""
        reviews = (
            Review.objects.filter(
                Q(user=config.request_user),
            )
            .distinct()
            .select_related("user")
        )
        reviews = reviews.annotate(editable=Value(True, output_field=BooleanField()))
        return reviews

    def get_posts(self, config: UserPostsConfig) -> list[Review | Ticket]:
        """Return the user's tickets and reviews sorted from newest to oldest."""
        merge_posts_config = MergePostsConfig(
            tickets=self.get_user_tickets(config),
            reviews=self.get_user_reviews(config),
        )

        return merge_posts(merge_posts_config)
