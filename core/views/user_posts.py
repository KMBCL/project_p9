from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render

from core.constants import TEMPLATE_PATHS
from core.data_managers.user_posts import UserPostsConfig, UserPostsService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class UserPostsView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        config = UserPostsConfig(request_user=request.user)
        service = UserPostsService()
        user_posts = service.get_posts(config)

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.USER_POSTS,
            context={"user_posts": user_posts},
        )
