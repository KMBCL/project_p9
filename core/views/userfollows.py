from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render, redirect


from core.constants import TEMPLATE_PATHS
from core.template_path_creator import TemplatePathCreator
from core.forms.following import FollowingForm
from core.forms.delete import DeleteForm

from core.data_managers.userfollows import (
    UserFollowsCreateConfig,
    UserFollowsCollectionConfig,
    UserFollowsDetailConfig,
    UserFollowsDeleteConfig,
    UserFollowsService,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from django.db.models import QuerySet

    from core.models.userfollows import UserFollows


def get_user_follows(request: HttpRequest, request_parameters: str) -> UserFollows | None:
    config = UserFollowsDetailConfig(
        request_user=request.user,
        request_parameters=request_parameters,
    )
    user_follows_service = UserFollowsService()
    user_follows = user_follows_service.get_user_follows(config)

    return user_follows


class UserFollowsView(View):

    def get_following_relations(self, request: HttpRequest) -> QuerySet[UserFollows, UserFollows]:
        collection_config = UserFollowsCollectionConfig(request_user=request.user)
        user_follows_service = UserFollowsService()
        return user_follows_service.get_following_relations(collection_config)

    def get_followed_by_relations(self, request: HttpRequest) -> QuerySet[UserFollows, UserFollows]:
        collection_config = UserFollowsCollectionConfig(request_user=request.user)
        user_follows_service = UserFollowsService()
        return user_follows_service.get_followed_by_relations(collection_config)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = FollowingForm()
        following_relations = self.get_following_relations(request)
        followed_by_relations = self.get_followed_by_relations(request)
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.USER_FOLLOWS,
            context={
                "form": form,
                "following_relations": following_relations,
                "followed_by_relations": followed_by_relations,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = FollowingForm(request.POST)
        if form.is_valid():
            config = UserFollowsCreateConfig(
                request_user=request.user,
                followed_username=form.cleaned_data["username"],
            )
            user_follows_service = UserFollowsService()

            try:
                user_follows_service.create_user_follows(config)

            except ValueError as error:
                form.add_error(None, str(error))

            else:
                return redirect("userfollows")

        following_relations = self.get_following_relations(request)
        followed_by_relations = self.get_followed_by_relations(request)
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.USER_FOLLOWS,
            context={
                "form": form,
                "following_relations": following_relations,
                "followed_by_relations": followed_by_relations,
            },
        )


class UserFollowsDeleteView(View):

    def get(self, request: HttpRequest, request_parameters: str) -> HttpResponse:
        form = DeleteForm()
        user_follows = get_user_follows(request, request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("userfollows"),
            context={
                "form": form,
                "user_follows": user_follows,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str) -> HttpResponse:
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = UserFollowsDeleteConfig(
                request_user=request.user,
                request_parameters=request_parameters,
            )
            user_follows_service = UserFollowsService()
            user_follows_service.delete_user_follows(config)

            return redirect("userfollows")

        user_follows = get_user_follows(request, request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("userfollows"),
            context={
                "form": form,
                "user_follows": user_follows,
            },
        )
