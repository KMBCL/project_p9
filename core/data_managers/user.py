from dataclasses import dataclass
from core.models.user import User


@dataclass
class RegistringUser:
    username: str
    password: str


class UserService:

    def __init__(self) -> None:
        pass

    def register_user(self, registring_user: RegistringUser):
        existing_user = User.objects.filter(username__iexact=registring_user.username).exists()
        if existing_user:
            raise ValueError("Nom d'utilisateur déjà existant!")

        try:
            user = User.objects.create_user(
                username=registring_user.username,
                password=registring_user.password,
            )
        except:
            raise ValueError("Echec création utilisateur!")

        return user
