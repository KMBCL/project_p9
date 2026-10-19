from __future__ import annotations

from datetime import datetime

from django.conf import settings
from django.db import models

from core.models.user import User


class Ticket(models.Model):
    title: models.CharField[str, str] = models.CharField(
        max_length=128,
    )
    description: models.TextField[str, str] = models.TextField(
        max_length=2048,
        blank=True,
    )
    user: models.ForeignKey[User, User] = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image: models.ImageField = models.ImageField(
        null=True,
        blank=True,
        upload_to="ticket/",
    )
    time_created: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True,
    )
