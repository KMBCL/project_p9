"""Constants shared across the core app."""

from enum import StrEnum

RATING_RANGE = range(1, 6)


class TEMPLATE_PATHS(StrEnum):
    """Paths of the templates rendered by non-CRUD views."""

    HOME_TEMPLATE_PATH = "core/home.html"
    REGISTER_TEMPLATE_PATH = "core/register/register.html"
    FEED = "core/feed.html"
    USER_POSTS = "core/user_posts.html"
    USER_FOLLOWS = "core/userfollows/userfollows.html"


class VIEW_TYPES(StrEnum):
    """Kinds of views, used to build CRUD template file names."""

    CREATE = "create"
    CREATE_FROM = "create_from"
    UPDATE = "update"
    DELETE = "delete"


class CONTENT_TYPE(StrEnum):
    """Types of posts that can appear in a feed."""

    REVIEW = "review"
    TICKET = "ticket"
