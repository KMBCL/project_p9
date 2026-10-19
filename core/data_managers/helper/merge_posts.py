from dataclasses import dataclass

from itertools import chain

from django.db.models import CharField, Value, QuerySet

from core.constants import CONTENT_TYPE
from core.models.ticket import Ticket
from core.models.review import Review


@dataclass
class MergePostsConfig:
    tickets: QuerySet[Ticket, Ticket]
    reviews: QuerySet[Review, Review]


def merge_posts(config: MergePostsConfig) -> list[Review | Ticket]:
    tickets = config.tickets
    reviews = config.reviews

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
