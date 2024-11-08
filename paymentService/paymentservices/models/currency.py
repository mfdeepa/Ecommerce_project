from django.db import models
from paymentservices.models.baseModel import BaseModel


class Currency(BaseModel):
    currency_tag = models.CharField(max_length=50)   # "INR", "USD", "EUR", "NPR"
    currency_name = models.CharField(max_length=50)   # "Indian Rupee", "USD Dollar"
    country = models.CharField(max_length=50)

