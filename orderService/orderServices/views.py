from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny

from . import models
from .models import Order, OrderItem, OrderStatusHistory, OrderTracking
from .serializers.serializer import CreateOrderSerializer, OrderSerializer, OrderSummarySerializer, \
    OrderTrackingSerializer


def get_user_id_from_request(request):
    # try:
    #     return request.auth.get('user_id') if request.auth else None
    # except AttributeError:
    #     return None
    return request.data.get('user_id')

class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user_id = get_user_id_from_request(self.request)
        # if not user_id:
        #     # This should ideally be caught by the permission class, but it's a good safeguard.
        #     raise ValidationError("User could not be identified from the request token.")

        # Save order with or without user ID
        order = serializer.save(user_id=user_id)  # Make sure serializer accepts `user_id`

        # order = serializer.save()

        # Create initial status history
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Order created',
            # created_by = models.ForeignKey(user_id, null=True, blank=True, on_delete=models.SET_NULL)
        )

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'order_number'
    queryset = Order.objects.all()


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSummarySerializer

    def get_queryset(self):
        user_id = get_user_id_from_request(self.request)
        queryset = Order.objects.filter(user_id=user_id)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset


@api_view(['POST'])
def cancel_order(request, order_number):
    """
    Cancels an order if it's in a cancellable state.
    """
    user_id = get_user_id_from_request(request)
    order = get_object_or_404(Order, order_number=order_number, user_id=user_id)

    if order.status in ['shipped', 'delivered', 'cancelled']:
        return Response(
            {'error': 'Order cannot be cancelled in its current status.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.status = 'cancelled'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        status='cancelled',
        notes='Order cancelled by customer.',
        created_by_id=user_id
    )

    return Response({'message': 'Order has been successfully cancelled.'})


@api_view(['POST'])
def update_order_status(request, order_number):
    """
    Admin endpoint to update any order's status.
    """
    admin_user_id = get_user_id_from_request(request)
    order = get_object_or_404(Order, order_number=order_number)

    new_status = request.data.get('status')
    if new_status not in dict(Order.ORDER_STATUS_CHOICES):
        return Response({'error': 'Invalid status provided.'}, status=status.HTTP_400_BAD_REQUEST)

    notes = request.data.get('notes', f'Status updated by admin.')
    old_status = order.status
    order.status = new_status

    if new_status == 'shipped' and old_status != 'shipped':
        order.shipped_at = timezone.now()
        order.tracking_number = request.data.get('tracking_number', order.tracking_number)
        order.carrier = request.data.get('carrier', order.carrier)
    elif new_status == 'delivered' and old_status != 'delivered':
        order.delivered_at = timezone.now()

    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        status=new_status,
        notes=notes,
        created_by_id=admin_user_id
    )

    # Send status update email (uncomment when ready)
    # send_order_status_update_email(order, old_status, new_status)

    return Response(OrderSerializer(order).data)
#
# class OrderTrackingView(generics.RetrieveAPIView):
#     serializer_class = OrderTrackingSerializer
#     lookup_field = 'order__order_number'
#
#     def get_queryset(self):
#         return OrderTracking.objects.filter(order__user=self.request.user)
#
#
# @api_view(['POST'])
# def confirm_order(request, order_number):
#     """Confirm order and update status"""
#     order = get_object_or_404(Order, order_number=order_number, user=request.user)
#
#     if order.status != 'pending':
#         return Response(
#             {'error': 'Order cannot be confirmed in current status'},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     order.status = 'confirmed'
#     order.confirmed_at = timezone.now()
#     order.save()
#
#     # Add status history
#     OrderStatusHistory.objects.create(
#         order=order,
#         status='confirmed',
#         notes='Order confirmed by user',
#         created_by=request.user
#     )
#
#     # Update tracking
#     if hasattr(order, 'tracking'):
#         order.tracking.add_tracking_event(
#             'payment_confirmed',
#             'Order confirmed and payment processed'
#         )
#
#     # Send confirmation email
#     send_order_confirmation_email(order)
#
#     return Response({'message': 'Order confirmed successfully'})
#
#
# @api_view(['POST'])
# def cancel_order(request, order_number):
#     """Cancel order if eligible"""
#     order = get_object_or_404(Order, order_number=order_number, user=request.user)
#
#     if order.status in ['shipped', 'delivered', 'cancelled']:
#         return Response(
#             {'error': 'Order cannot be cancelled in current status'},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     order.status = 'cancelled'
#     order.save()
#
#     # Add status history
#     OrderStatusHistory.objects.create(
#         order=order,
#         status='cancelled',
#         notes='Order cancelled by user',
#         created_by=request.user
#     )
#
#     return Response({'message': 'Order cancelled successfully'})
#
#
# @api_view(['POST'])
# def update_order_status(request, order_number):
#     """Admin endpoint to update order status"""
#     # This would typically require admin permissions
#     order = get_object_or_404(Order, order_number=order_number)
#
#     new_status = request.data.get('status')
#     notes = request.data.get('notes', '')
#     tracking_number = request.data.get('tracking_number')
#     carrier = request.data.get('carrier')
#
#     if new_status not in dict(Order.ORDER_STATUS_CHOICES):
#         return Response(
#             {'error': 'Invalid status'},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     old_status = order.status
#     order.status = new_status
#
#     # Update timestamps based on status
#     if new_status == 'shipped' and old_status != 'shipped':
#         order.shipped_at = timezone.now()
#         if tracking_number:
#             order.tracking_number = tracking_number
#         if carrier:
#             order.carrier = carrier
#     elif new_status == 'delivered' and old_status != 'delivered':
#         order.delivered_at = timezone.now()
#
#     order.save()
#
#     # Add status history
#     OrderStatusHistory.objects.create(
#         order=order,
#         status=new_status,
#         notes=notes,
#         created_by=request.user if request.user.is_authenticated else None
#     )
#
#     # Update tracking
#     if hasattr(order, 'tracking'):
#         tracking_messages = {
#             'confirmed': 'Order confirmed and being processed',
#             'processing': 'Order is being prepared for shipment',
#             'shipped': f'Order shipped via {carrier}' if carrier else 'Order has been shipped',
#             'delivered': 'Order has been delivered',
#             'cancelled': 'Order has been cancelled'
#         }
#
#         if new_status in tracking_messages:
#             order.tracking.add_tracking_event(
#                 new_status,
#                 tracking_messages[new_status]
#             )
#
#     # Send status update email
#     send_order_status_update_email(order, old_status, new_status)
#
#     return Response({'message': 'Order status updated successfully'})
#
#
# @api_view(['GET'])
# def order_statistics(request):
#     """Get user's order statistics"""
#     user_orders = Order.objects.filter(user=request.user)
#
#     stats = {
#         'total_orders': user_orders.count(),
#         'pending_orders': user_orders.filter(status='pending').count(),
#         'completed_orders': user_orders.filter(status='delivered').count(),
#         'cancelled_orders': user_orders.filter(status='cancelled').count(),
#         'total_spent': sum(order.total_amount for order in user_orders),
#     }
#
#     return Response(stats)
#
#
# @api_view(['POST'])
# def test_create_order(request):
#     """Simple test endpoint to debug order creation"""
#     try:
#         data = request.data
#         print(f"Received data: {data}")
#
#         # Create order manually for testing
#         order = Order.objects.create(
#             user=request.user,
#             total_amount=data.get('total_amount', 0),
#             tax_amount=data.get('tax_amount', 0),
#             shipping_amount=data.get('shipping_amount', 0),
#             discount_amount=data.get('discount_amount', 0),
#             shipping_address=data.get('shipping_address', {}),
#             billing_address=data.get('billing_address', data.get('shipping_address', {})),
#             notes=data.get('notes', ''),
#         )
#
#         # Create order items
#         items_data = data.get('items', [])
#         for item_data in items_data:
#             OrderItem.objects.create(
#                 order=order,
#                 product_id=item_data.get('product_id', ''),
#                 product_name=item_data.get('product_name', ''),
#                 product_sku=item_data.get('product_sku', ''),
#                 quantity=item_data.get('quantity', 1),
#                 unit_price=item_data.get('unit_price', 0),
#             )
#
#         # Create tracking
#         OrderTracking.objects.create(order=order)
#
#         return Response({
#             'success': True,
#             'order_id': str(order.id),
#             'order_number': order.order_number,
#             'message': 'Order created successfully'
#         })
#
#     except Exception as e:
#         print(f"Error in test_create_order: {e}")
#         import traceback
#         traceback.print_exc()
#         return Response({
#             'success': False,
#             'error': str(e)
#         }, status=500)
#
#
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
#
#
# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email,
#             'username': user.username
#         })
#
#
# @api_view(['POST'])
# def register_user(request):
#     """Register a new user"""
#     try:
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         if not all([username, email, password]):
#             return Response(
#                 {'error': 'Username, email, and password are required'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         if User.objects.filter(username=username).exists():
#             return Response(
#                 {'error': 'Username already exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )
#
#         token, created = Token.objects.get_or_create(user=user)
#
#         return Response({
#             'message': 'User created successfully',
#             'token': token.key,
#             'user_id': user.pk,
#             'username': user.username,
#             'email': user.email
#         }, status=status.HTTP_201_CREATED)
#
#     except Exception as e:
#         return Response(
#             {'error': str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
