import uuid

from django.db import models
from payments.models import BasePayment


class BaseModel(BasePayment):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #transaction_id = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


