from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    @property
    def normalized_username(self) -> str:
        return self.username.upper()
