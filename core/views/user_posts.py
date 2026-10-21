"""View displaying the tickets and reviews posted by a user."""

from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render

from core.constants import RATING_RANGE, TEMPLATE_PATHS
from core.data_managers.user_posts import UserPostsConfig, UserPostsService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class UserPostsView(View):
    """Displays the user's own tickets and reviews."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the user's posts sorted from newest to oldest."""
        config = UserPostsConfig(request_user=request.user)
        service = UserPostsService()
        user_posts = service.get_posts(config)

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.USER_POSTS,
            context={
                "user_posts": user_posts,
                "rating_range": RATING_RANGE,
            },
        )
