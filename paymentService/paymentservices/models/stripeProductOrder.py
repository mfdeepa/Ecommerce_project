from paymentservices.models.baseModel import BaseModel
from django.db import models


class StripeProductOrder(BaseModel):
    product_id = models.IntegerField(max_length=255, unique=True)
    stripe_price_id = models.CharField(max_length=255, unique=True)
    stripe_product_id = models.CharField(max_length=255, unique=True)
