from core.constants import VIEW_TYPES


class URLShortcutCreator:

    @staticmethod
    def create(model_name: str):
        return f"{model_name}_{VIEW_TYPES.CREATE}"

    @staticmethod
    def collection(model_name: str):
        return f"{model_name}_{VIEW_TYPES.COLLECTION}"

    @staticmethod
    def detail(model_name: str):
        return f"{model_name}_{VIEW_TYPES.DETAIL}"

    @staticmethod
    def update(model_name: str):
        return f"{model_name}_{VIEW_TYPES.UPDATE}"

    @staticmethod
    def delete(model_name: str):
        return f"{model_name}_{VIEW_TYPES.DELETE}"
