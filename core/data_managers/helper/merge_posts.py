"""Helper merging tickets and reviews into a single chronological list."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass

from itertools import chain

from django.db.models import CharField, Value

from core.constants import CONTENT_TYPE

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from core.models.ticket import Ticket
    from core.models.review import Review


@dataclass
class MergePostsConfig:
    """Input data for merging tickets and reviews into a feed."""

    tickets: QuerySet[Ticket, Ticket]
    reviews: QuerySet[Review, Review]


def merge_posts(config: MergePostsConfig) -> list[Review | Ticket]:
    """Tag tickets and reviews with their content type and sort them from newest to oldest."""
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
