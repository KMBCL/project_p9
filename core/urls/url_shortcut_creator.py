from core.constants import VIEW_TYPES


class URLShortcutCreator:

    @staticmethod
    def create(model_name: str) -> str:
        return f"{model_name}_{VIEW_TYPES.CREATE}"

    @staticmethod
    def create_from(model_name: str) -> str:
        return f"{model_name}_{VIEW_TYPES.CREATE_FROM}"

    @staticmethod
    def update(model_name: str) -> str:
        return f"{model_name}_{VIEW_TYPES.UPDATE}"

    @staticmethod
    def delete(model_name: str) -> str:
        return f"{model_name}_{VIEW_TYPES.DELETE}"
