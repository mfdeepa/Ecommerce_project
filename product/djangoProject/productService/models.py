
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(null=False, blank=False)


class Product(BaseModel):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    #image_url = models.ImageField(default='default.jpg', upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)


class Rating(models.Model):
    rate = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return f"Rating: {self.rate}, Count: {self.count}"
