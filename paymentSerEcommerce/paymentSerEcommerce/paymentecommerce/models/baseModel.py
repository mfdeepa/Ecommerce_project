import uuid

from django.db import models
from payments.models import BasePayment


class BaseModel(BasePayment):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
