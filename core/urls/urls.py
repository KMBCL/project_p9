from django.urls import path, URLPattern, URLResolver
from django.contrib.auth.decorators import login_required

from core.urls.url_creator import URLCreator
from core.urls.url_shortcut_creator import URLShortcutCreator

from core.views.authentication import home_view, login_view, logout_view
from core.views.register import RegisterView
import core.views.ticket as TicketViews
import core.views.review as ReviewViews

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
        URLCreator.detail("ticket"),
        login_required(TicketViews.TicketDetailView.as_view()),
        name=URLShortcutCreator.detail("ticket"),
    ),
    path(
        URLCreator.update("ticket"),
        login_required(TicketViews.TicketUpdateView.as_view()),
        name=URLShortcutCreator.update("ticket"),
    ),
    path(
        URLCreator.delete("ticket"),
        TicketViews.TicketDeleteView.as_view(),
        name=URLShortcutCreator.delete("ticket"),
    ),
]

review_urlpatterns:list[URLPattern|URLResolver]=[
    path(
        URLCreator.create_from("review"),
        login_required(ReviewViews.ReviewCreateFromView.as_view()),
        name=URLShortcutCreator.
    )
]

core_urlpatterns: list[URLPattern | URLResolver] = []
core_urlpatterns.extend(urlpatterns)
core_urlpatterns.extend(ticket_urlpatterns)
