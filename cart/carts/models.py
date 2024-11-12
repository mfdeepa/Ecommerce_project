from django.db import models
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission


class CartCustomUser(AbstractUser):
    # Add your custom fields
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Use a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Use a unique related_name
        blank=True
    )


class Product(models.Model):
    """Product model for validation and inventory checking"""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.PositiveIntegerField(default=0)

    def check_inventory(self, requested_quantity):
        return self.inventory_count >= requested_quantity

    def reserve_inventory(self, quantity):
        if self.inventory_count >= quantity:
            self.inventory_count -= quantity
            self.save()
            return True
        return False


class Discount(models.Model):
    """Discount model for handling various types of discounts"""
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
    max_uses = models.PositiveIntegerField(default=None, null=True)
    current_uses = models.PositiveIntegerField(default=0)

    def is_valid(self, cart_total):
        now = timezone.now()
        return (
                self.valid_from <= now <= self.valid_until and
                cart_total >= self.min_purchase_amount and
                (self.max_uses is None or self.current_uses < self.max_uses)
        )

    def calculate_discount(self, cart_total):
        if self.discount_type == 'percentage':
            return (cart_total * self.value) / 100
        elif self.discount_type == 'fixed':
            return min(self.value, cart_total)
        return Decimal('0.00')


class Cart(models.Model):
    user = models.ForeignKey(CartCustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
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


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subtotal(self):
        return self.price * self.quantity
