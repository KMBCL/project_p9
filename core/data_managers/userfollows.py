from dataclasses import dataclass

from typing import Any

from django.db.models import QuerySet
from core.models.user import User
from core.models.userfollows import UserFollows


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
    request_parameters: str


@dataclass
class UserFollowsDeleteConfig:
    request_user: User
    request_parameters: str


class UserFollowsService:

    def __init__(self) -> None:
        pass

    def get_followed_user(self, followed_username: str) -> User | None:
        followed_user = User.objects.filter(
            username=followed_username,
        ).first()
        return followed_user

    def create_user_follows(self, config: UserFollowsCreateConfig):
        followed_user = self.get_followed_user(config.followed_username)

        if followed_user is None:
            return None

        user_follows = UserFollows.objects.create(
            user=config.request_user,
            followed_user=followed_user,
        )

        return user_follows

    def get_following_relations(self, config: UserFollowsCollectionConfig):
        following_users = UserFollows.objects.filter(user=config.request_user).select_related()
        return following_users

    def get_followed_by_relations(self, config: UserFollowsCollectionConfig):
        followed_by_users = UserFollows.objects.filter(followed_user=config.request_user).select_related()
        return followed_by_users

    def get_user_follows(self, config: UserFollowsDetailConfig):
        user_follows = (
            UserFollows.objects.filter(
                user=config.request_user,
                pk=int(config.request_parameters),
            )
            .select_related()
            .first()
        )
        return user_follows

    def delete_user_follows(self, config: UserFollowsDeleteConfig) -> None:
        user_follows = UserFollows.objects.filter(
            user=config.request_user,
            pk=config.request_parameters,
        ).first()

        if user_follows is None:
            return None

        user_follows.delete()
