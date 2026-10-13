from django.urls import path, URLPattern, URLResolver
from django.contrib.auth.decorators import login_required

from core.urls.url_creator import URLCreator
from core.urls.url_shortcut_creator import URLShortcutCreator

from core.views.authentication import home_view, logout_view
from core.views.register import RegisterView
from core.views.feed import FeedView
from core.views.user_posts import UserPostsView


import core.views.ticket as TicketViews
import core.views.review as ReviewViews
import core.views.userfollows as UserFollowsViews

urlpatterns: list[URLPattern | URLResolver] = [
    path("home/", home_view, name="home"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("feed/", login_required(FeedView.as_view()), name="feed"),
    path("user_posts/", login_required(UserPostsView.as_view()), name="user_posts"),
]

ticket_urlpatterns: list[URLPattern | URLResolver] = [
    path(
        URLCreator.create("ticket"),
        login_required(
            TicketViews.TicketCreateView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.create("ticket"),
    ),
    path(
        URLCreator.update("ticket"),
        login_required(
            TicketViews.TicketUpdateView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.update("ticket"),
    ),
    path(
        URLCreator.delete("ticket"),
        login_required(
            TicketViews.TicketDeleteView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.delete("ticket"),
    ),
]

review_urlpatterns: list[URLPattern | URLResolver] = [
    path(
        URLCreator.create("review"),
        login_required(
            ReviewViews.ReviewCreateView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.create("review"),
    ),
    path(
        URLCreator.create_from("review"),
        login_required(
            ReviewViews.ReviewCreateFromView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.create_from("review"),
    ),
    path(
        URLCreator.update("review"),
        login_required(
            ReviewViews.ReviewUpdateView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.update("review"),
    ),
    path(
        URLCreator.delete("review"),
        login_required(
            ReviewViews.ReviewDeleteView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.delete("review"),
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
        URLCreator.delete("userfollows"),
        login_required(
            UserFollowsViews.UserFollowsDeleteView.as_view(),
            login_url="home",
        ),
        name=URLShortcutCreator.delete("userfollows"),
    ),
]

core_urlpatterns: list[URLPattern | URLResolver] = []
core_urlpatterns.extend(urlpatterns)
core_urlpatterns.extend(ticket_urlpatterns)
core_urlpatterns.extend(review_urlpatterns)
core_urlpatterns.extend(user_follows_urlpattenrs)
