from django.db import models
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission

class Product(models.Model):

    product_id = models.IntegerField(unique=True, null=True, blank=True)  # From product-service
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def check_inventory(self, requested_quantity):
        return self.inventory_count >= requested_quantity


class Discount(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('buy_x_get_y', 'Buy X Get Y'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    current_uses = models.PositiveIntegerField(default=0)

    def is_valid(self, cart_total):
        now = timezone.now()
        return (
            self.valid_from <= now <= self.valid_until and
            cart_total >= self.min_purchase_amount and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )

    def calculate_discount(self, cart_total):
        if cart_total <= 0:
            return Decimal('0.00')
        if self.discount_type == 'percentage':
            return (cart_total * self.value) / 100
        elif self.discount_type == 'fixed':
            return min(self.value, cart_total)
        return Decimal('0.00')

    def __str__(self):
        return self.code


class Cart(models.Model):

    user_id = models.IntegerField(null=True, blank=True)  # from user service
    session_id = models.CharField(max_length=255, null=True, blank=True)  # for guest users (if needed)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)  # Default 7-day expiration
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total(self):
        subtotal = self.get_subtotal()
        if self.discount and self.discount.is_valid(subtotal):
            return subtotal - self.discount.calculate_discount(subtotal)
        return subtotal

    def __str__(self):
        return f"Cart {self.id} for User {self.user_id or 'Guest'}"

class CartItem(models.Model):

    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField(default=0)  # no FK to local Product model
    title = models.CharField(max_length=255, default="Unnamed Product")  # snapshot of product name/title
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # snapshot of price
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.title} (ID: {self.product_id}) in Cart {self.cart_id}"
