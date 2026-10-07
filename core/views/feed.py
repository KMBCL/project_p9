from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render, redirect

from core.constants import TEMPLATE_PATHS

if TYPE_CHECKING:
    from django.http import HttpRequest


class FeedView(View):

    def get(self, request: HttpRequest):

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.FEED,
            context={},
        )
