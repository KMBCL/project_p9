from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from core.forms.authentication import AuthenticationForm
from core.constants import TEMPLATE_PATHS

if TYPE_CHECKING:
    from django.http import HttpResponse


# def home_view(request: Any) -> HttpResponse:
#     return render(
#         request=request,
#         template_name=TEMPLATE_PATHS.HOME_TEMPLATE_PATH,
#         context={},
#     )


def home_view(request: Any) -> HttpResponse:
    if request.method == "GET":
        form = AuthenticationForm()
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.HOME_TEMPLATE_PATH,
            context={"form": form},
        )
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("feed")
        return redirect("login")


def logout_view(request: Any) -> HttpResponse:
    return render(
        request=request,
        template_name=TEMPLATE_PATHS.HOME_TEMPLATE_PATH,
        context={},
    )
