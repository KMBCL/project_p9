"""Helper building template paths for model CRUD views."""

from core.constants import VIEW_TYPES


class TemplatePathCreator:
    """Builds template paths of the form core/<model_name>/<view_type>.html."""

    @staticmethod
    def create(model_name: str) -> str:
        """Return the path of the model's creation template."""
        return f"core/{model_name}/{VIEW_TYPES.CREATE}.html"

    @staticmethod
    def create_from(model_name: str) -> str:
        """Return the path of the model's create-from-ticket template."""
        return f"core/{model_name}/{VIEW_TYPES.CREATE_FROM}.html"

    @staticmethod
    def update(model_name: str) -> str:
        """Return the path of the model's update template."""
        return f"core/{model_name}/{VIEW_TYPES.UPDATE}.html"

    @staticmethod
    def delete(model_name: str) -> str:
        """Return the path of the model's deletion template."""
        return f"core/{model_name}/{VIEW_TYPES.DELETE}.html"
