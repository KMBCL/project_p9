"""View displaying the feed of tickets and reviews visible to a user."""

from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render

from core.constants import RATING_RANGE, TEMPLATE_PATHS
from core.data_managers.feed import FeedConfig, FeedService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class FeedView(View):
    """Displays the user's feed of tickets and reviews."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the feed sorted from newest to oldest."""
        config = FeedConfig(request_user=request.user)
        service = FeedService()
        feed = service.get_feed(config)

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.FEED,
            context={
                "feed": feed,
                "rating_range": RATING_RANGE,
            },
        )
