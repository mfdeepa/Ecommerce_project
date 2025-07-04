from django.db import models
from decimal import Decimal
import uuid
from django.core.validators import RegexValidator


def generate_order_number():
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cod', 'Cash on Delivery'),
    ]

    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    user_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    shipping_address = models.JSONField()
    billing_address = models.JSONField()
    phone_number = models.CharField(
        max_length=10,
        validators=[phone_validator],
        verbose_name="Customer Phone Number",
        null=True,
        blank=True,
    )

    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    customer_snapshot = models.JSONField(default=dict, blank=True)

    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    carrier = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['status']),
            models.Index(fields=['order_number']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        # Calculate total if not set
        if self.pk and not self.total_amount:
            self.calculate_total()
        super().save(*args, **kwargs)

    def calculate_total(self):
        """Calculate order total from items"""
        self.subtotal = sum(item.get_subtotal() for item in self.items.all())
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    product_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    product_snapshot = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['order', 'product_id']

    def get_subtotal(self):
        return self.price * self.quantity

    @property
    def subtotal(self):
        return self.get_subtotal()

    def __str__(self):
        return f"{self.quantity} x {self.title} in {self.order.order_number}"


class OrderTracking(models.Model):
    order = models.OneToOneField(Order, related_name='tracking', on_delete=models.CASCADE)

    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    carrier = models.CharField(max_length=50, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)

    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)

    current_location = models.CharField(max_length=255, blank=True, null=True)
    tracking_events = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking for {self.order.order_number}"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name='status_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_by_id = models.IntegerField(null=True, blank=True)  # User who made the change
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Order status histories"

    def __str__(self):
        return f"{self.order.order_number} - {self.status} at {self.created_at}"


class OrderNote(models.Model):
    order = models.ForeignKey(Order, related_name='order_notes', on_delete=models.CASCADE)
    note = models.TextField()
    is_internal = models.BooleanField(default=False)  # Internal notes not visible to customer
    created_by_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.order.order_number}"
