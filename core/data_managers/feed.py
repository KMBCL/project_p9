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
    request_user: User


class FeedService:

    def _get_user_reviews(self, config: FeedConfig) -> QuerySet[Review, Review]:
        """Gets user reviews related to loaded tickets."""
        return Review.objects.filter(
            user=config.request_user,
            ticket=OuterRef("pk"),
        )

    def _get_tickets(self, config: FeedConfig) -> QuerySet[Ticket, Ticket]:
        """Gets tickets :
        user__followed_by__user traverses:
            Ticket.user
            -> UserFollows where Ticket.user is followed_user
            -> UserFollows.user, the follower

            Q() allows boolean combinations such as OR with |

            Visible tickets:
            - tickets created by request_user
            - tickets created by users followed by request_user
        """
        return (
            Ticket.objects.filter(
                Q(user=config.request_user) | Q(user__followed_by__user=config.request_user),
            )
            .distinct()
            .select_related("user")  # préciser quoi remonter
        )

    def get_viewable_tickets(self, config: FeedConfig) -> QuerySet[Ticket, Ticket]:
        """Gets viewable annotated tickets."""

        user_reviews = self._get_user_reviews(config)
        tickets = self._get_tickets(config)
        tickets = tickets.annotate(has_user_reviews=Exists(user_reviews))
        return tickets

    def get_viewable_reviews(self, config: FeedConfig) -> QuerySet[Review, Review]:
        """
        User
        Following users
        Reviews for request_user tickets.
        """

        reviews = (
            Review.objects.filter(
                Q(user=config.request_user)
                | Q(user__followed_by__user=config.request_user)
                | Q(ticket__user=config.request_user)
            )
            .distinct()
            .select_related()
        )
        return reviews

    def get_feed(self, config: FeedConfig) -> list[Review | Ticket]:
        merge_posts_config = MergePostsConfig(
            tickets=self.get_viewable_tickets(config),
            reviews=self.get_viewable_reviews(config),
        )

        return merge_posts(merge_posts_config)
