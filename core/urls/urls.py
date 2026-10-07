from django.urls import path, URLPattern, URLResolver
from django.contrib.auth.decorators import login_required

from core.urls.url_creator import URLCreator
from core.urls.url_shortcut_creator import URLShortcutCreator

from core.views.authentication import home_view, login_view, logout_view
from core.views.register import RegisterView


import core.views.ticket as TicketViews
import core.views.review as ReviewViews
import core.views.userfollows as UserFollowsViews

urlpatterns: list[URLPattern | URLResolver] = [
    path("home/", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]

ticket_urlpatterns: list[URLPattern | URLResolver] = [
    path(
        URLCreator.create("ticket"),
        login_required(TicketViews.TicketCreateView.as_view()),
        name=URLShortcutCreator.create("ticket"),
    ),
    path(
        URLCreator.collection("ticket"),
        login_required(TicketViews.TicketCollectionView.as_view()),
        name=URLShortcutCreator.collection("ticket"),
    ),
    path(
        URLCreator.update("ticket"),
        login_required(TicketViews.TicketUpdateView.as_view()),
        name=URLShortcutCreator.update("ticket"),
    ),
    path(
        URLCreator.delete("ticket"),
        login_required(TicketViews.TicketDeleteView.as_view()),
        name=URLShortcutCreator.delete("ticket"),
    ),
]

review_urlpatterns: list[URLPattern | URLResolver] = [
    path(
        URLCreator.create_from("review"),
        login_required(ReviewViews.ReviewCreateFromView.as_view()),
        name=URLShortcutCreator.create_from("review"),
    ),
    path(
        URLCreator.collection("review"),
        login_required(ReviewViews.ReviewCollectionView.as_view()),
        name=URLShortcutCreator.collection("review"),
    ),
    path(
        URLCreator.detail("review"),
        login_required(ReviewViews.ReviewDetailView.as_view()),
        name=URLShortcutCreator.detail("review"),
    ),
    path(
        URLCreator.update("review"),
        login_required(ReviewViews.ReviewUpdateView.as_view()),
        name=URLShortcutCreator.update("review"),
    ),
    path(
        URLCreator.delete("review"),
        login_required(ReviewViews.ReviewDeleteView.as_view()),
        name=URLShortcutCreator.delete("review"),
    ),
]

user_follows_urlpattenrs: list[URLPattern | URLResolver] = [
    path(
        URLCreator.create("userfollows"),
        login_required(UserFollowsViews.UserFollowsCreateView.as_view()),
        name=URLShortcutCreator.create("userfollows"),
    ),
    path(
        URLCreator.delete("userfollows"),
        login_required(UserFollowsViews.UserFollowsDeleteView.as_view()),
        name=URLShortcutCreator.delete("userfollows"),
    ),
]

core_urlpatterns: list[URLPattern | URLResolver] = []
core_urlpatterns.extend(urlpatterns)
core_urlpatterns.extend(ticket_urlpatterns)
core_urlpatterns.extend(review_urlpatterns)
core_urlpatterns.extend(user_follows_urlpattenrs)
