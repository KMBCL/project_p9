from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import path
from django.contrib.auth.decorators import login_required

from core.views.authentication import home_view, logout_view
from core.views.register import RegisterView
from core.views.feed import FeedView
from core.views.user_posts import UserPostsView


import core.views.ticket as TicketViews
import core.views.review as ReviewViews
import core.views.userfollows as UserFollowsViews

if TYPE_CHECKING:
    from django.urls import URLPattern, URLResolver

urlpatterns: list[URLPattern | URLResolver] = [
    path("home/", home_view, name="home"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("feed/", login_required(FeedView.as_view()), name="feed"),
    path("user_posts/", login_required(UserPostsView.as_view()), name="user_posts"),
]

ticket_urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "ticket/create/",
        login_required(
            TicketViews.TicketCreateView.as_view(),
            login_url="home",
        ),
        name="ticket_create",
    ),
    path(
        "ticket/update/<int:pk>/",
        login_required(
            TicketViews.TicketUpdateView.as_view(),
            login_url="home",
        ),
        name="ticket_update",
    ),
    path(
        "ticket/delete/<int:pk>/",
        login_required(
            TicketViews.TicketDeleteView.as_view(),
            login_url="home",
        ),
        name="ticket_delete",
    ),
]

review_urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "review/create/",
        login_required(
            ReviewViews.ReviewCreateView.as_view(),
            login_url="home",
        ),
        name="review_create",
    ),
    path(
        "review/create_from/<int:pk>/",
        login_required(
            ReviewViews.ReviewCreateFromView.as_view(),
            login_url="home",
        ),
        name="review_create_from",
    ),
    path(
        "review/update/<int:pk>/",
        login_required(
            ReviewViews.ReviewUpdateView.as_view(),
            login_url="home",
        ),
        name="review_update",
    ),
    path(
        "review/delete/<int:pk>/",
        login_required(
            ReviewViews.ReviewDeleteView.as_view(),
            login_url="home",
        ),
        name="review_delete",
    ),
]

user_follows_urlpattenrs: list[URLPattern | URLResolver] = [
    path(
        "userfollows/",
        login_required(
            UserFollowsViews.UserFollowsView.as_view(),
            login_url="home",
        ),
        name="userfollows",
    ),
    path(
        "userfollows/delete/<int:pk>/",
        login_required(
            UserFollowsViews.UserFollowsDeleteView.as_view(),
            login_url="home",
        ),
        name="userfollows_delete",
    ),
]

core_urlpatterns: list[URLPattern | URLResolver] = []
core_urlpatterns.extend(urlpatterns)
core_urlpatterns.extend(ticket_urlpatterns)
core_urlpatterns.extend(review_urlpatterns)
core_urlpatterns.extend(user_follows_urlpattenrs)
