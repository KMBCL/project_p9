"""Custom user model of the application."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Application user, extending Django's default user."""

    @property
    def normalized_username(self) -> str:
        """Return the username in uppercase."""
        return self.username.upper()
