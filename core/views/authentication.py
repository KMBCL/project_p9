from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpResponse

HOME_TEMPLATE_PATH = "core/home.html"
LOGIN_TEMPLATE_PATH = "core/login.html"
LOGOUT_TEMPLATE_PATH = "core/logout.html"


def home(request: Any) -> HttpResponse:

    return render(request=request, template_name=HOME_TEMPLATE_PATH, context={})


def login(request: Any) -> HttpResponse:
    user = authenticate(username="john", credentials="test")

    return render(request=request, template_name=LOGIN_TEMPLATE_PATH, context={})


def logout(request: Any) -> HttpResponse:

    return render(request=request, template_name=HOME_TEMPLATE_PATH, context={})
