from core.constants import VIEW_TYPES


class URLCreator:

    @staticmethod
    def create(model_name: str) -> str:
        return f"{model_name}/{VIEW_TYPES.CREATE}/"

    @staticmethod
    def create_from(model_name: str) -> str:
        return f"{model_name}/{VIEW_TYPES.CREATE_FROM}/<str:request_parameters>/"

    @staticmethod
    def update(model_name: str) -> str:
        return f"{model_name}/{VIEW_TYPES.UPDATE}/<str:request_parameters>/"

    @staticmethod
    def delete(model_name: str) -> str:
        return f"{model_name}/{VIEW_TYPES.DELETE}/<str:request_parameters>/"
