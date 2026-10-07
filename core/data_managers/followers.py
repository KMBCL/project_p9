from dataclasses import dataclass

from typing import Any

from django.db.models import QuerySet
from core.models.user import User
from core.models.userfollows import UserFollows


@dataclass
class UserFollowsCreateConfig:
    request_user: User
    following_username: str


@dataclass
class UserFollowsCollectionConfig:
    request_user: User


class UserFollowsService:

    def __init__(self) -> None:
        pass

    def create_user_follows(self, config: UserFollowsCreateConfig):
        following_user = User.objects.filter(
            username=config.following_username,
        ).first()

        if following_user is None:
            return None

        print("user", config.request_user.username)
        print("following user", following_user.username)

        user_follows = UserFollows.objects.create(
            user=config.request_user,
            followed_user=following_user,
        )

        return user_follows

    def get_user_follows(self, config: UserFollowsCollectionConfig):
        user_follows = UserFollows.objects.filter(user=config.request_user)
        return user_follows
