from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from core.forms.authentication import AuthenticationForm, RegisterForm

if TYPE_CHECKING:
    from django.http import HttpResponse

HOME_TEMPLATE_PATH = "core/home.html"
LOGIN_TEMPLATE_PATH = "core/login.html"
LOGOUT_TEMPLATE_PATH = "core/logout.html"
REGISTER_TEMPLATE_PATH = "core/register.html"


def home_view(request: Any) -> HttpResponse:
    return render(
        request=request,
        template_name=HOME_TEMPLATE_PATH,
        context={},
    )


def login_view(request: Any) -> HttpResponse:
    if request.method == "GET":
        form = AuthenticationForm()
        return render(
            request=request,
            template_name=LOGIN_TEMPLATE_PATH,
            context={"form": form},
        )
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        return redirect("login")


def logout_view(request: Any) -> HttpResponse:
    return render(request=request, template_name=HOME_TEMPLATE_PATH, context={})


def register_view(request: Any) -> HttpResponse:
    if request.method == "GET":
        form = RegisterForm()
        return render(
            request=request,
            template_name=REGISTER_TEMPLATE_PATH,
            context={"form": form},
        )
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Fucking registered user!")
            return redirect("login")

        return render(
            request=request,
            template_name=REGISTER_TEMPLATE_PATH,
            context={"form": form},
        )
