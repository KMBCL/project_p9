from __future__ import annotations

from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


from core.models.user import User
from core.models.ticket import Ticket


class Review(models.Model):
    ticket: models.ForeignKey[Ticket, Ticket] = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
    )
    rating: models.PositiveSmallIntegerField[int, int] = (
        models.PositiveSmallIntegerField(
            validators=[
                MinValueValidator(0),
                MaxValueValidator(5),
            ]
        )
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
