from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render, redirect

from core.template_path_creator import TemplatePathCreator

from core.forms.review import ReviewForm
from core.forms.delete import DeleteForm
from core.data_managers.review import (
    ReviewCreateConfig,
    ReviewCollectionConfig,
    ReviewService,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from core.models.review import Review


class ReviewCreateFromView(View):
    def get(self, request: HttpRequest, request_parameters: str):
        form = ReviewForm()

        return render(
            request=request,
            template_name=TemplatePathCreator.create("review"),
            context={"form": form},
        )

    def post(self, request: HttpRequest, request_parameters: str):
        form = ReviewForm(request.POST)
        if form.is_valid():
            config = ReviewCreateConfig(
                ticket_pk=int(request_parameters),
                rating=int(form.cleaned_data["rating"]),
                headline=form.cleaned_data["headline"],
                body=form.cleaned_data["body"],
                request_user=request.user,
            )
            review_service = ReviewService()
            review_service.create_review(config)
            return redirect("review_collection")

        return render(
            request=request,
            template_name=TemplatePathCreator.create("review"),
            context={"form": form},
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
    pass


class ReviewDeleteView(View):
    pass
