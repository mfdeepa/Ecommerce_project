from typing import Optional

from django.db import models

from userservices.models import User


class UserManager(models.Manager):
    def findByEmail(self, email: str) -> Optional[User]:
        pass
