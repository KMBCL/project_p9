"""Views for creating, updating and deleting reviews."""

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
    ReviewDetailConfig,
    ReviewUpdateConfig,
    ReviewDeleteConfig,
    ReviewService,
)
from core.data_managers.ticket import TicketDetailConfig, TicketService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from core.models.review import Review
    from core.models.ticket import Ticket


def get_user_review(request: HttpRequest, pk: int) -> Review | None:
    """Return the review owned by the requesting user, or None."""
    config = ReviewDetailConfig(
        request_user=request.user,
        pk=pk,
    )
    service = ReviewService()
    review = service.get_user_review(config)
    return review


class ReviewCreateView(View):
    """Creates a ticket together with its review."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render empty ticket and review forms."""
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

    def post(self, request: HttpRequest) -> HttpResponse:
        """Create the ticket and its review, or re-render the forms with errors."""
        ticket_form = TicketForm(
            request.POST or None,
            request.FILES or None,
            prefix="ticket",
        )
        review_form = ReviewForm(
            request.POST or None,
            prefix="review",
        )

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
            service.create_review_and_ticket(config)

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
    """Creates a review in response to an existing ticket."""

    def get_ticket(self, request: HttpRequest, pk: int) -> Ticket | None:
        """Return the ticket being reviewed, or None."""
        ticket_config = TicketDetailConfig(
            request_user=request.user,
            pk=pk,
        )
        ticket_service = TicketService()
        return ticket_service.get_ticket(ticket_config)

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render an empty review form alongside the ticket."""
        form = ReviewForm()
        ticket = self.get_ticket(request, pk)
        return render(
            request=request,
            template_name=TemplatePathCreator.create_from("review"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Create the review for the ticket, or re-render the form with errors."""
        form = ReviewForm(request.POST)
        if form.is_valid():
            config = ReviewCreateFromConfig(
                ticket_pk=pk,
                rating=int(form.cleaned_data["rating"]),
                headline=form.cleaned_data["headline"],
                body=form.cleaned_data["body"],
                request_user=request.user,
            )
            review_service = ReviewService()
            review_service.create_review_from_ticket(config)
            return redirect("feed")

        ticket = self.get_ticket(request, pk)
        return render(
            request=request,
            template_name=TemplatePathCreator.create_from("review"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )


class ReviewUpdateView(View):
    """Updates a review owned by the user."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render the review form pre-filled with the existing review."""
        review = get_user_review(request, pk)
        form = ReviewForm(instance=review)
        ticket = review.ticket if review is not None else None
        return render(
            request=request,
            template_name=TemplatePathCreator.update("review"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Update the review, or re-render the form with errors."""
        form = ReviewForm(request.POST)
        if form.is_valid():
            config = ReviewUpdateConfig(request_user=request.user, pk=pk, cleaned_data=form.cleaned_data)
            ticket_service = ReviewService()
            ticket_service.update_review(config)
            return redirect("user_posts")

        review = get_user_review(request, pk)
        ticket = review.ticket if review is not None else None
        return render(
            request=request,
            template_name=TemplatePathCreator.update("review"),
            context={
                "form": form,
                "ticket": ticket,
            },
        )


class ReviewDeleteView(View):
    """Deletes a review owned by the user after confirmation."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render the deletion confirmation page."""
        form = DeleteForm()
        review = get_user_review(request, pk)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("review"),
            context={
                "form": form,
                "review": review,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Delete the review, or re-render the confirmation page with errors."""
        form = DeleteForm(request.POST)
        if form.is_valid():
            config = ReviewDeleteConfig(
                request_user=request.user,
                pk=pk,
            )
            review_service = ReviewService()
            review_service.delete_review(config)

            return redirect("user_posts")

        review = get_user_review(request, pk)

        return render(
            request=request,
            template_name=TemplatePathCreator.delete("review"),
            context={
                "form": form,
                "review": review,
            },
        )
