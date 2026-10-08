from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render, redirect


from core.constants import TEMPLATE_PATHS
from core.template_path_creator import TemplatePathCreator
from core.forms.following import FollowingForm
from core.forms.delete import DeleteForm

from core.data_managers.followers import (
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


class UserFollowsCreateView(View):

    def get_user_follows(self, request: HttpRequest) -> QuerySet[UserFollows, UserFollows]:
        collection_config = UserFollowsCollectionConfig(request_user=request.user)
        user_follows_service = UserFollowsService()
        return user_follows_service.get_following_relations(collection_config)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = FollowingForm()
        user_follows = self.get_user_follows(request)
        return render(
            request=request,
            template_name=TemplatePathCreator.create("userfollows"),
            context={
                "form": form,
                "user_follows": user_follows,
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
            user_follows_service.create_user_follows(config)
            return redirect("userfollows_create")

        user_follows = self.get_user_follows(request)
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.FOLLOWING_TEMPLATE_PATH,
            context={
                "form": form,
                "user_follows": user_follows,
            },
        )


class UserFollowsDeleteView(View):

    def get_user_follows(self, request_parameters: str) -> UserFollows | None:
        config = UserFollowsDetailConfig(pk=request_parameters)
        user_follows_service = UserFollowsService()
        user_follows = user_follows_service.get_user_follows(config)

        return user_follows

    def get(self, request: HttpRequest, request_parameters: str):
        form = DeleteForm()
        ticket = self.get_user_follows(request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str):
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = UserFollowsDeleteConfig(pk=request_parameters)
            ticket_service = UserFollowsService()
            ticket_service.delete_user_follows(config)

            return redirect("userfollows_create")

        ticket = self.get_user_follows(request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("ticket"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )
