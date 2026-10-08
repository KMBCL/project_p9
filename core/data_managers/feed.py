from dataclasses import dataclass
from itertools import chain

from django.db.models import Q, CharField, Value, Prefetch, Exists, OuterRef

from core.constants import CONTENT_TYPE
from core.models.user import User
from core.models.userfollows import UserFollows
from core.models.ticket import Ticket
from core.models.review import Review


@dataclass
class FeedConfig:
    request_user: User


class FeedService:

    def get_viewable_tickets(self, config: FeedConfig):
        # user__followed_by__user traverses:
        # Ticket.user
        # -> UserFollows where Ticket.user is followed_user
        # -> UserFollows.user, the follower
        #
        # Q() allows boolean combinations such as OR with |
        #
        # Visible tickets:
        # - tickets created by request_user
        # - tickets created by users followed by request_user
        user_reviews = Review.objects.filter(
            user=config.request_user,
            ticket=OuterRef("pk"),
        )
        tickets = Ticket.objects.filter(
            Q(user=config.request_user) | Q(user__followed_by__user=config.request_user),
        ).select_related()
        tickets = tickets.annotate(has_user_reviews=Exists(user_reviews))
        return tickets

    def get_viewable_reviews(self, config: FeedConfig):
        # User
        # Following users
        # Reviews for request_user tickets.

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

    def get_feed(self, config: FeedConfig):
        tickets = self.get_viewable_tickets(config)
        reviews = self.get_viewable_reviews(config)

        tickets = tickets.annotate(
            content_type=Value(
                CONTENT_TYPE.TICKET,
                CharField(),
            )
        )
        reviews = reviews.annotate(
            content_type=Value(
                CONTENT_TYPE.REVIEW,
                CharField(),
            )
        )

        feed = sorted(
            chain(reviews, tickets),
            key=lambda feed: feed.time_created,
            reverse=True,
        )
        return feed
