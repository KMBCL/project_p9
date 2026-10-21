"""Function views handling user login and logout."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from core.forms.authentication import AuthenticationForm
from core.constants import TEMPLATE_PATHS

if TYPE_CHECKING:
    from django.http import HttpResponse


def home_view(request: Any) -> HttpResponse:
    """Display the login form and authenticate the user on submission."""
    if request.method == "GET":
        form = AuthenticationForm()
        return render(
            request=request,
            template_name=TEMPLATE_PATHS.HOME_TEMPLATE_PATH,
            context={"form": form},
        )
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("feed")
            form.add_error(None, "Identifiants incorrects.")

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.HOME_TEMPLATE_PATH,
            context={"form": form},
        )

    return redirect("home")


def logout_view(request: Any) -> HttpResponse:
    """Log the user out, clear their session and redirect to the home page."""
    request.session.delete()
    logout(request)
    return redirect("home")
