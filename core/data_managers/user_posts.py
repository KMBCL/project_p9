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
    request_user: User


class UserPostsService:

    def get_user_tickets(self, config: UserPostsConfig) -> QuerySet[Ticket, Ticket]:
        user_reviews = Review.objects.filter(
            user=config.request_user,
            ticket=OuterRef("pk"),
        )
        tickets = Ticket.objects.filter(Q(user=config.request_user)).select_related()
        tickets = tickets.annotate(has_user_reviews=Exists(user_reviews))
        tickets = tickets.annotate(editable=Value(True, output_field=BooleanField()))
        return tickets

    def get_user_reviews(self, config: UserPostsConfig) -> QuerySet[Review, Review]:
        reviews = (
            Review.objects.filter(
                Q(user=config.request_user),
            )
            .distinct()
            .select_related()
        )
        reviews = reviews.annotate(editable=Value(True, output_field=BooleanField()))
        return reviews

    def get_posts(self, config: UserPostsConfig) -> list[Review | Ticket]:
        merge_posts_config = MergePostsConfig(
            tickets=self.get_user_tickets(config),
            reviews=self.get_user_reviews(config),
        )

        return merge_posts(merge_posts_config)
