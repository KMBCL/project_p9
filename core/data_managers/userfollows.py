from __future__ import annotations

from typing import TYPE_CHECKING

from dataclasses import dataclass


from core.models.user import User
from core.models.userfollows import UserFollows

if TYPE_CHECKING:
    from django.db.models import QuerySet


@dataclass
class UserFollowsCreateConfig:
    request_user: User
    followed_username: str


@dataclass
class UserFollowsCollectionConfig:
    request_user: User


@dataclass
class UserFollowsDetailConfig:
    request_user: User
    pk: int


@dataclass
class UserFollowsDeleteConfig:
    request_user: User
    pk: int


class UserFollowsService:

    def __init__(self) -> None:
        pass

    def get_followed_user(self, followed_username: str) -> User | None:
        followed_user = User.objects.filter(
            username=followed_username,
        ).first()
        return followed_user

    def create_user_follows(self, config: UserFollowsCreateConfig) -> UserFollows:
        followed_user = self.get_followed_user(config.followed_username)

        if followed_user is None:
            raise ValueError("Utilisateur inexistant!")

        user_follows = UserFollows.objects.create(
            user=config.request_user,
            followed_user=followed_user,
        )

        return user_follows

    def get_following_relations(self, config: UserFollowsCollectionConfig) -> QuerySet[UserFollows, UserFollows]:
        following_users = UserFollows.objects.filter(user=config.request_user).select_related()
        return following_users

    def get_followed_by_relations(self, config: UserFollowsCollectionConfig) -> QuerySet[UserFollows, UserFollows]:
        followed_by_users = UserFollows.objects.filter(followed_user=config.request_user).select_related()
        return followed_by_users

    def get_user_follows(self, config: UserFollowsDetailConfig) -> UserFollows | None:
        user_follows = (
            UserFollows.objects.filter(
                user=config.request_user,
                pk=config.pk,
            )
            .select_related()
            .first()
        )
        return user_follows

    def delete_user_follows(self, config: UserFollowsDeleteConfig) -> None:
        user_follows = UserFollows.objects.filter(
            user=config.request_user,
            pk=config.pk,
        ).first()

        if user_follows is None:
            return None

        user_follows.delete()
