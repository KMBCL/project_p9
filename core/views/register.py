from __future__ import annotations

from typing import TYPE_CHECKING


from django.views import View
from django.shortcuts import render, redirect

from core.forms.register import RegisterForm
from core.constants import TEMPLATE_PATHS


from core.data_managers.user import RegistringUser, UserService

if TYPE_CHECKING:
    from django.http import HttpRequest


class RegisterView(View):

    def get(self, request: HttpRequest):
        form = RegisterForm()

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.REGISTER_TEMPLATE_PATH,
            context={"form": form},
        )

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        if form.is_valid():
            registring_user = RegistringUser(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
            )
            user_service = UserService()
            user_service.register_user(registring_user)
            return redirect("login")

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.REGISTER_TEMPLATE_PATH,
            context={"form": form},
        )
