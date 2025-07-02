from django.db import models

from paymentecommerce.models.baseModel import BaseModel


class StripeProductOrder(BaseModel):
    prod_id = models.IntegerField(unique=True)
    stripe_price_id = models.CharField(max_length=255, unique=True)
    stripe_product_id = models.CharField(max_length=255, unique=True)