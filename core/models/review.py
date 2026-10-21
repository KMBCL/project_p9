"""Model representing a review written by a user about a ticket."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


from core.models.ticket import Ticket

if TYPE_CHECKING:
    from datetime import datetime
    from core.models.user import User


class Review(models.Model):
    """A user's rated review of a ticket, with a headline and an optional body."""

    ticket: models.ForeignKey[Ticket, Ticket] = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
    )
    rating: models.PositiveSmallIntegerField[int, int] = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    headline: models.CharField[str, str] = models.CharField(
        max_length=128,
    )
    body: models.CharField[str, str] = models.CharField(
        max_length=8192,
        blank=True,
    )
    user: models.ForeignKey[User, User] = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    time_created: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True,
    )
