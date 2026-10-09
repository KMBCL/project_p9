from enum import StrEnum


class TEMPLATE_PATHS(StrEnum):
    HOME_TEMPLATE_PATH = "core/home.html"
    LOGIN_TEMPLATE_PATH = "core/authentication/login.html"
    LOGOUT_TEMPLATE_PATH = "core/authentication/logout.html"
    REGISTER_TEMPLATE_PATH = "core/register/register.html"
    FEED = "core/feed.html"
    USER_POSTS = "core/user_posts.html"
    USER_FOLLOWS = "core/userfollows/userfollows.html"


class VIEW_TYPES(StrEnum):
    CREATE = "create"
    CREATE_FROM = "create_from"
    COLLECTION = "collection"
    DETAIL = "detail"
    UPDATE = "update"
    DELETE = "delete"


class CONTENT_TYPE(StrEnum):
    REVIEW = "review"
    TICKET = "ticket"
