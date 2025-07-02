from typing import List

from django.db import models

from userservices.models import Role


class RoleManager(models.Manager):
    def find_all_by_ids(self, role_ids: List) -> [Role]:
        pass
