"""Service building the feed of tickets and reviews visible to a user."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from django.db.models import Q, Exists, OuterRef

from core.models.ticket import Ticket
from core.models.review import Review
from core.data_managers.helper.merge_posts import MergePostsConfig, merge_posts

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from core.models.user import User


@dataclass
class FeedConfig:
    """Input data for building a user's feed."""

    request_user: User


class FeedService:
    """Retrieves the tickets and reviews visible to a user and merges them into a feed."""

    def _get_user_reviews(self, config: FeedConfig) -> QuerySet[Review, Review]:
        """Build a subquery of the user's reviews on the outer ticket."""
        return Review.objects.filter(
            user=config.request_user,
            ticket=OuterRef("pk"),
        )

    def _get_tickets(self, config: FeedConfig) -> QuerySet[Ticket, Ticket]:
        """Return the tickets created by the user or by users they follow.

        user__followed_by__user traverses:
            Ticket.user
            -> UserFollows where Ticket.user is followed_user
            -> UserFollows.user, the follower

        Q() allows boolean combinations such as OR with |.
        """
        return (
            Ticket.objects.filter(
                Q(user=config.request_user) | Q(user__followed_by__user=config.request_user),
            )
            .distinct()
            .select_related("user")
        )

    def get_viewable_tickets(self, config: FeedConfig) -> QuerySet[Ticket, Ticket]:
        """Return the visible tickets, annotated with whether the user has reviewed them."""
        user_reviews = self._get_user_reviews(config)
        tickets = self._get_tickets(config)
        tickets = tickets.annotate(has_user_reviews=Exists(user_reviews))
        return tickets

    def get_viewable_reviews(self, config: FeedConfig) -> QuerySet[Review, Review]:
        """Return the user's reviews, those of followed users, and reviews on the user's tickets."""
        reviews = (
            Review.objects.filter(
                Q(user=config.request_user)
                | Q(user__followed_by__user=config.request_user)
                | Q(ticket__user=config.request_user)
            )
            .distinct()
            .select_related("user")
        )
        return reviews

    def get_feed(self, config: FeedConfig) -> list[Review | Ticket]:
        """Return the visible tickets and reviews sorted from newest to oldest."""
        merge_posts_config = MergePostsConfig(
            tickets=self.get_viewable_tickets(config),
            reviews=self.get_viewable_reviews(config),
        )

        return merge_posts(merge_posts_config)
