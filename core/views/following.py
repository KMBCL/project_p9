from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render, redirect


from core.constants import TEMPLATE_PATHS
from core.forms.following import FollowingForm
from core.data_managers.followers import (
    UserFollowsCreateConfig,
    UserFollowsCollectionConfig,
    UserFollowsService,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from django.db.models import QuerySet

    from core.models.userfollows import UserFollows


class FollowingView(View):

    def get_user_follows(self, request: HttpRequest) -> QuerySet[UserFollows, UserFollows]:
        collection_config = UserFollowsCollectionConfig(request_user=request.user)
        user_follows_service = UserFollowsService()
        return user_follows_service.get_user_follows(collection_config)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = FollowingForm()
        user_follows = self.get_user_follows(request)
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.FOLLOWING_TEMPLATE_PATH,
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
                following_username=form.cleaned_data["username"],
            )
            user_follows_service = UserFollowsService()
            user_follows_service.create_user_follows(config)
            return redirect("following")

        user_follows = self.get_user_follows(request)
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.FOLLOWING_TEMPLATE_PATH,
            context={
                "form": form,
                "user_follows": user_follows,
            },
        )
