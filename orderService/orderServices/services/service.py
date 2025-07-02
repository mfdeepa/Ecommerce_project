from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from dateutil.parser import parse
from orderServices.models import Order, OrderItem, OrderTracking, OrderStatusHistory
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class OrderService:
    @transaction.atomic
    def create_order(self, validated_data, customer_snapshot):
        logger.info(f"OrderService.create_order called with: {validated_data}")

        try:
            items_data = validated_data.pop('items', [])
            shipping_address = validated_data.get('shipping_address', {})
            billing_address = validated_data.get('billing_address', shipping_address)

            order_data = {
                'user_id': validated_data['user_id'],
                'status': 'pending',
                'payment_method': validated_data.get('payment_method', 'card'),
                'subtotal': 0,
                'shipping_cost': 0,
                'tax_amount': 0,
                'total_amount': 0,
                'shipping_address': shipping_address,
                'billing_address': billing_address,
                'customer_snapshot': customer_snapshot
            }

            logger.info(f"Creating order with data: {order_data}")
            order = Order.objects.create(**order_data)
            logger.info(f"Order created with ID: {order.id}")

            total_subtotal = 0
            for item_data in items_data:
                logger.info(f"Creating item: {item_data}")

                item_total = float(item_data['price']) * item_data['quantity']
                total_subtotal += item_total
                snapshot = item_data.copy()
                snapshot['price'] = float(snapshot['price'])

                OrderItem.objects.create(
                    order=order,
                    product_id=item_data['product_id'],
                    title=item_data['title'],
                    price=item_data['price'],
                    quantity=item_data['quantity'],
                    product_snapshot=snapshot
                )

            shipping_cost = 10.00
            tax_amount = total_subtotal * 0.08
            total_amount = total_subtotal + shipping_cost + tax_amount

            order.subtotal = total_subtotal
            order.shipping_cost = shipping_cost
            order.tax_amount = tax_amount
            order.total_amount = total_amount
            order.save()

            logger.info(f"Order updated with totals: {total_amount}")
            return order

        except Exception as e:
            logger.error(f"Error in OrderService.create_order: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def cancel_order(self, order_number, user_id):
        order = get_object_or_404(Order, order_number=order_number, user_id=user_id)

        if order.status in ['shipped', 'delivered', 'cancelled']:
            raise ValidationError("Order cannot be cancelled in its current status.")

        order.status = 'cancelled'
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status='cancelled',
            notes='Order cancelled by user',
            created_by_id=user_id
        )

        return order

    def update_order_status(self, order_number, new_status, admin_user_id, tracking_data=None, notes=None):
        order = get_object_or_404(Order, order_number=order_number)

        if new_status not in dict(Order.ORDER_STATUS_CHOICES):
            raise ValidationError("Invalid status value.")

        old_status = order.status
        order.status = new_status

        if new_status == 'shipped' and old_status != 'shipped':
            order.shipped_at = timezone.now()
            if tracking_data:
                order.tracking_number = tracking_data.get('tracking_number', order.tracking_number)
                order.carrier = tracking_data.get('carrier', order.carrier)

        elif new_status == 'delivered' and old_status != 'delivered':
            order.delivered_at = timezone.now()

        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            notes=notes or "Updated by admin.",
            created_by_id=admin_user_id
        )

        return order

    def get_order_history(self, user_id, filters=None):
        if not user_id:
            raise ValidationError("User ID is required.")

        queryset = Order.objects.filter(user_id=user_id)

        if filters:
            if filters.get("status"):
                queryset = queryset.filter(status=filters["status"])
            if filters.get("date_from"):
                try:
                    date_from = parse(filters["date_from"])
                    queryset = queryset.filter(created_at__gte=date_from)
                except Exception as e:
                    raise ValidationError(f"Invalid date_from format: {e}")
            if filters.get("date_to"):
                queryset = queryset.filter(created_at__lte=filters["date_to"])

        return queryset

    def get_order_by_number(self, order_number, user_id=None):
        order = get_object_or_404(Order, order_number=order_number)
        if user_id and order.user_id != user_id:
            raise PermissionDenied("You do not have permission to access this order.")
        return order
