from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render, redirect

from core.template_path_creator import TemplatePathCreator

from core.forms.review import ReviewForm
from core.forms.ticket import TicketForm
from core.forms.delete import DeleteForm
from core.data_managers.review import (
    ReviewCreateConfig,
    ReviewCreateFromConfig,
    ReviewCollectionConfig,
    ReviewDetailConfig,
    ReviewUpdateConfig,
    ReviewDeleteConfig,
    ReviewService,
)
from core.data_managers.ticket import TicketDetailConfig, TickeService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from core.models.review import Review


def get_user_review(request: HttpRequest, request_parameters: str):
    config = ReviewDetailConfig(
        request_user=request.user,
        request_parameter=request_parameters,
    )
    service = ReviewService()
    review = service.get_user_review(config)
    return review


class ReviewCreateView(View):
    def get(self, request: HttpRequest):
        ticket_form = TicketForm(prefix="ticket")
        review_form = ReviewForm(prefix="review")

        return render(
            request=request,
            template_name=TemplatePathCreator.create("review"),
            context={
                "ticket_form": ticket_form,
                "review_form": review_form,
            },
        )

    def post(self, request: HttpRequest):
        ticket_form = TicketForm(request.POST or None, prefix="ticket")
        review_form = ReviewForm(request.POST or None, prefix="review")

        if ticket_form.is_valid() and review_form.is_valid():
            config = ReviewCreateConfig(
                request_user=request.user,
                ticket_title=ticket_form.cleaned_data["title"],
                ticket_description=ticket_form.cleaned_data["description"],
                ticket_image=ticket_form.cleaned_data["image"],
                review_headline=review_form.cleaned_data["headline"],
                review_rating=review_form.cleaned_data["rating"],
                review_body=review_form.cleaned_data["body"],
            )
            service = ReviewService()
            service.create_review(config)

            return redirect("feed")

        return render(
            request=request,
            template_name=TemplatePathCreator.create("review"),
            context={
                "ticket_form": ticket_form,
                "review_form": review_form,
            },
        )


class ReviewCreateFromView(View):

    def get_ticket(self, request: HttpRequest, request_parameters: str):
        ticket_config = TicketDetailConfig(
            request_user=request.user,
            request_parameter=request_parameters,
        )
        ticket_service = TickeService()
        return ticket_service.get_ticket(ticket_config)

    def get(self, request: HttpRequest, request_parameters: str):
        form = ReviewForm()
        ticket = self.get_ticket(request, request_parameters)
        return render(
            request=request,
            template_name=TemplatePathCreator.create_from("review"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str):
        form = ReviewForm(request.POST)
        if form.is_valid():
            config = ReviewCreateFromConfig(
                ticket_pk=int(request_parameters),
                rating=int(form.cleaned_data["rating"]),
                headline=form.cleaned_data["headline"],
                body=form.cleaned_data["body"],
                request_user=request.user,
            )
            review_service = ReviewService()
            review_service.create_from_review(config)
            return redirect("feed")

        ticket = self.get_ticket(request, request_parameters)
        return render(
            request=request,
            template_name=TemplatePathCreator.create_from("review"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )


class ReviewCollectionView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        config = ReviewCollectionConfig(request_user=request.user)
        review_service = ReviewService()
        reviews = review_service.get_reviews(config)

        return render(
            request=request,
            template_name=TemplatePathCreator.collection("review"),
            context={"reviews": reviews},
        )


class ReviewDetailView(View):
    pass


class ReviewUpdateView(View):

    def get(self, request: HttpRequest, request_parameters: str):
        review = get_user_review(request, request_parameters)
        form = ReviewForm(instance=review)
        ticket = review.ticket if review is not None else None
        return render(
            request=request,
            template_name=TemplatePathCreator.update("review"),
            context={
                "form": form,
                "reviewed_ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str):
        form = ReviewForm(request.POST)
        if form.is_valid():
            config = ReviewUpdateConfig(
                request_user=request.user, request_parameter=request_parameters, cleaned_data=form.cleaned_data
            )
            ticket_service = ReviewService()
            ticket_service.update_review(config)
            return redirect("user_posts")

        review = get_user_review(request, request_parameters)
        ticket = review.ticket if review is not None else None
        return render(
            request=request,
            template_name=TemplatePathCreator.update("review"),
            context={
                "form": form,
                "reviewed_ticket": ticket,
            },
        )


class ReviewDeleteView(View):

    def get(self, request: HttpRequest, request_parameters: str):
        form = DeleteForm()
        review = get_user_review(request, request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("review"),
            context={
                "form": form,
                "review": review,
            },
        )

    def post(self, request: HttpRequest, request_parameters: str):
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = ReviewDeleteConfig(
                request_user=request.user,
                request_parameter=request_parameters,
            )
            review_service = ReviewService()
            review_service.delete_review(config)

            return redirect("user_posts")

        review = get_user_review(request, request_parameters)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("review"),
            context={
                "form": form,
                "review": review,
            },
        )
