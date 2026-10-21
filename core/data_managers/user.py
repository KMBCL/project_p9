"""Service handling user registration."""

from dataclasses import dataclass

from django.db import IntegrityError

from core.models.user import User


@dataclass
class RegistringUser:
    """Credentials of a user being registered."""

    username: str
    password: str


class UserService:
    """Handles user account creation."""

    def __init__(self) -> None:
        pass

    def register_user(self, registring_user: RegistringUser) -> User:
        """Create a new user, raising ValueError if the username is taken or creation fails."""
        existing_user = User.objects.filter(username__iexact=registring_user.username).exists()
        if existing_user:
            raise ValueError("Nom d'utilisateur déjà existant!")

        try:
            user = User.objects.create_user(
                username=registring_user.username,
                password=registring_user.password,
            )
        except IntegrityError as error:
            raise ValueError("Echec création utilisateur!") from error

        return user
