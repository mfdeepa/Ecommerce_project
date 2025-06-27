from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id):
    """Send order confirmation email asynchronously"""
    try:
        from .models import Order
        order = Order.objects.get(id=order_id)

        subject = f'Order Confirmation - {order.order_number}'
        message = f'''
        Dear {order.user.first_name or order.user.username},

        Thank you for your order! Here are the details:

        Order Number: {order.order_number}
        Order Date: {order.created_at.strftime('%B %d, %Y')}
        Total Amount: ${order.total_amount}
        Status: {order.get_status_display()}

        Items:
        '''

        for item in order.items.all():
            message += f'\n- {item.product_name} x {item.quantity} = ${item.total_price}'

        message += f'''

        Shipping Address:
        {order.shipping_address.get('name', '')}
        {order.shipping_address.get('address_line_1', '')}
        {order.shipping_address.get('address_line_2', '')}
        {order.shipping_address.get('city', '')}, {order.shipping_address.get('state', '')} {order.shipping_address.get('postal_code', '')}

        You can track your order at: /orders/{order.order_number}/tracking

        Thank you for shopping with us!
        '''

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False,
        )

    except Exception as e:
        print(f"Error sending confirmation email: {e}")


def send_order_confirmation_email(order):
    """Wrapper function to send confirmation email"""
    send_order_confirmation_email.delay(order.id)


@shared_task
def send_order_status_update_email(order_id, old_status, new_status):
    """Send order status update email"""
    try:
        from .models import Order
        order = Order.objects.get(id=order_id)

        subject = f'Order Update - {order.order_number}'
        message = f'''
        Dear {order.user.first_name or order.user.username},

        Your order status has been updated:

        Order Number: {order.order_number}
        Previous Status: {old_status.title()}
        New Status: {new_status.title()}

        '''

        if new_status == 'shipped' and order.tracking_number:
            message += f'Tracking Number: {order.tracking_number}\n'
            message += f'Carrier: {order.carrier}\n'

        message += f'''
        You can track your order at: /orders/{order.order_number}/tracking

        Thank you for shopping with us!
        '''

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False,
        )

    except Exception as e:
        print(f"Error sending status update email: {e}")


def send_order_status_update_email(order, old_status, new_status):
    """Wrapper function to send status update email"""
    send_order_status_update_email.delay(order.id, old_status, new_status)