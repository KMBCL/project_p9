from enum import StrEnum


class TEMPLATE_PATHS(StrEnum):
    HOME_TEMPLATE_PATH = "core/home.html"
    LOGIN_TEMPLATE_PATH = "core/authentication/login.html"
    LOGOUT_TEMPLATE_PATH = "core/authentication/logout.html"
    REGISTER_TEMPLATE_PATH = "core/register/register.html"
    FOLLOWING_TEMPLATE_PATH = "core/followers/following.html"
    FEED = "core/feed.html"


class VIEW_TYPES(StrEnum):
    CREATE = "create"
    CREATE_FROM = "create_from"
    COLLECTION = "collection"
    DETAIL = "detail"
    UPDATE = "update"
    DELETE = "delete"
