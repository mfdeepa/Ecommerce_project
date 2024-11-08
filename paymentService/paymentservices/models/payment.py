import uuid

from django.db import models
from payments.models import BasePayment

from paymentservices.models.paymentGatewayType import PaymentGatewayType


class Payment(BasePayment):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=250, blank=True, null=True)
    payment_link = models.CharField(max_length=250, blank=True, null=True)
    payment_gateway = models.CharField(
        max_length=250,
        choices=[(gateway.value[0], gateway.value[1]) for gateway in PaymentGatewayType],
        default=PaymentGatewayType.STRIPE.value[0]
    )
