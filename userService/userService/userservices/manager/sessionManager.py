from typing import Optional

from django.db import models

from userservices.models import Session


class SessionManager(models.Manager):
    def findByTokenAndUserId(self, token, userId) -> Optional[Session]:
        pass
