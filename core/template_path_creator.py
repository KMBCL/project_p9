from core.constants import VIEW_TYPES


class TemplatePathCreator:

    @staticmethod
    def create(model_name: str) -> str:
        return f"core/{model_name}/{VIEW_TYPES.CREATE}.html"

    @staticmethod
    def create_from(model_name: str) -> str:
        return f"core/{model_name}/{VIEW_TYPES.CREATE_FROM}.html"

    @staticmethod
    def collection(model_name: str) -> str:
        return f"core/{model_name}/{VIEW_TYPES.COLLECTION}.html"

    @staticmethod
    def detail(model_name: str) -> str:
        return f"core/{model_name}/{VIEW_TYPES.DETAIL}.html"

    @staticmethod
    def update(model_name: str) -> str:
        return f"core/{model_name}/{VIEW_TYPES.UPDATE}.html"

    @staticmethod
    def delete(model_name: str) -> str:
        return f"core/{model_name}/{VIEW_TYPES.DELETE}.html"
