from django.http import HttpRequest

from django.views import View
from django.shortcuts import render, redirect

from core.forms.register import RegisterForm
from core.constants import TEMPLATE_PATHS


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
            print("Fucking registered user!")
            return redirect("login")

        return render(
            request=request,
            template_name=TEMPLATE_PATHS.REGISTER_TEMPLATE_PATH,
            context={"form": form},
        )
