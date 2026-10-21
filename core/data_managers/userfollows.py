"""Services and configurations for managing user follow relations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass


from core.models.user import User
from core.models.userfollows import UserFollows

if TYPE_CHECKING:
    from django.db.models import QuerySet


@dataclass
class UserFollowsCreateConfig:
    """Input data for following a user by username."""

    request_user: User
    followed_username: str


@dataclass
class UserFollowsCollectionConfig:
    """Input data for listing a user's follow relations."""

    request_user: User


@dataclass
class UserFollowsDetailConfig:
    """Input data for retrieving a single follow relation."""

    request_user: User
    pk: int


@dataclass
class UserFollowsDeleteConfig:
    """Input data for removing a follow relation."""

    request_user: User
    pk: int


class UserFollowsService:
    """Handles creation, retrieval and deletion of follow relations between users."""

    def __init__(self) -> None:
        pass

    def get_followed_user(self, followed_username: str) -> User | None:
        """Return the user matching the username, or None."""
        followed_user = User.objects.filter(
            username=followed_username,
        ).first()
        return followed_user

    def create_user_follows(self, config: UserFollowsCreateConfig) -> UserFollows:
        """Make the user follow another user, raising ValueError if they do not exist."""
        followed_user = self.get_followed_user(config.followed_username)

        if followed_user is None:
            raise ValueError("Utilisateur inexistant!")

        user_follows = UserFollows.objects.create(
            user=config.request_user,
            followed_user=followed_user,
        )

        return user_follows

    def get_following_relations(self, config: UserFollowsCollectionConfig) -> QuerySet[UserFollows, UserFollows]:
        """Return the relations of users followed by the user."""
        following_users = UserFollows.objects.filter(user=config.request_user).select_related()
        return following_users

    def get_followed_by_relations(self, config: UserFollowsCollectionConfig) -> QuerySet[UserFollows, UserFollows]:
        """Return the relations of users following the user."""
        followed_by_users = UserFollows.objects.filter(followed_user=config.request_user).select_related()
        return followed_by_users

    def get_user_follows(self, config: UserFollowsDetailConfig) -> UserFollows | None:
        """Return a follow relation owned by the user, or None."""
        user_follows = (
            UserFollows.objects.filter(
                user=config.request_user,
                pk=config.pk,
            )
            .select_related("user")
            .first()
        )
        return user_follows

    def delete_user_follows(self, config: UserFollowsDeleteConfig) -> None:
        """Delete a follow relation owned by the user."""
        user_follows = UserFollows.objects.filter(
            user=config.request_user,
            pk=config.pk,
        ).first()

        if user_follows is None:
            return None

        user_follows.delete()
