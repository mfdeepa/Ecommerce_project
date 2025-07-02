from django.db import models
from payments.models import BasePayment

from paymentecommerce.models.paymentGatewayType import PaymentGatewayType


class Payment(BasePayment):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.IntegerField(null=True, blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    transaction_id = models.CharField(max_length=250, blank=True, null=True)
    payment_link = models.CharField(max_length=250, blank=True, null=True)
    payment_gateway = models.CharField(
        max_length=250,
        choices=[(gateway.value[0], gateway.value[1]) for gateway in PaymentGatewayType],
        default=PaymentGatewayType.STRIPE.value[0]
    )
