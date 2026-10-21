"""Views for managing user follow relations."""

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


def get_user_follows(request: HttpRequest, pk: int) -> UserFollows | None:
    """Return the follow relation owned by the requesting user, or None."""
    config = UserFollowsDetailConfig(
        request_user=request.user,
        pk=pk,
    )
    user_follows_service = UserFollowsService()
    user_follows = user_follows_service.get_user_follows(config)

    return user_follows


class UserFollowsView(View):
    """Displays the user's follow relations and lets them follow other users."""

    def get_following_relations(self, request: HttpRequest) -> QuerySet[UserFollows, UserFollows]:
        """Return the relations of users followed by the user."""
        collection_config = UserFollowsCollectionConfig(request_user=request.user)
        user_follows_service = UserFollowsService()
        return user_follows_service.get_following_relations(collection_config)

    def get_followed_by_relations(self, request: HttpRequest) -> QuerySet[UserFollows, UserFollows]:
        """Return the relations of users following the user."""
        collection_config = UserFollowsCollectionConfig(request_user=request.user)
        user_follows_service = UserFollowsService()
        return user_follows_service.get_followed_by_relations(collection_config)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the follow form with the user's follow relations."""
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
        """Follow the given user, or re-render the page with errors."""
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
    """Removes a follow relation after confirmation."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render the unfollow confirmation page."""
        form = DeleteForm()
        user_follows = get_user_follows(request, pk)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("userfollows"),
            context={
                "form": form,
                "user_follows": user_follows,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Delete the follow relation, or re-render the confirmation page with errors."""
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = UserFollowsDeleteConfig(
                request_user=request.user,
                pk=pk,
            )
            user_follows_service = UserFollowsService()
            user_follows_service.delete_user_follows(config)

            return redirect("userfollows")

        user_follows = get_user_follows(request, pk)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("userfollows"),
            context={
                "form": form,
                "user_follows": user_follows,
            },
        )
