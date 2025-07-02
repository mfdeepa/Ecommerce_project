import logger
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound, PermissionDenied
from django.utils import timezone
from django.conf import settings
import logging

from ..models import Order
from ..services.service import OrderService
from ..services.user_validation import UserAuthValidator

DEBUG = getattr(settings, 'DEBUG', False)


try:
    from orderServices.serializers.serializer import (
        OrderItemSerializer,
        OrderItemCreateSerializer,
        OrderTrackingSerializer,
        OrderStatusHistorySerializer,
        OrderSerializer,
        OrderCreateSerializer,
        OrderUpdateStatusSerializer,
    )

except ImportError as e:
    logger.error(f"Failed to import serializers: {e}")

logger = logging.getLogger(__name__)


def authenticate_user(request):

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthenticationFailed("Authorization header is required.")

    if not auth_header.startswith('Bearer '):
        raise AuthenticationFailed("Invalid authorization header format. Use 'Bearer <token>'.")

    token = auth_header.split(' ')[1]
    user_data = UserAuthValidator.validate_token(token)
    return user_data


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):

    try:
        user_data = authenticate_user(request)
        user_id = user_data.get('user_id')

        data = request.data.copy()
        data['user_id'] = user_id

        serializer = OrderCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        order_service = OrderService()
        order = order_service.create_order(
            validated_data=serializer.validated_data,
            customer_snapshot=user_data
        )

        response_serializer = OrderSerializer(order)
        return Response({
            'message': 'Order created successfully',
            'order': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    except AuthenticationFailed as e:
        return Response({
            'error': 'Authentication failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

    except ValidationError as e:
        return Response({
            'error': 'Validation error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Unexpected error in create_order: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_order_history(request):

    try:
        logger.info("Starting get_order_history request")

        try:
            user_data = authenticate_user(request)
            user_id = user_data.get('user_id')
            logger.info(f"Authenticated user_id: {user_id}")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed(str(e))

        filters = {}
        if request.GET.get('status'):
            filters['status'] = request.GET.get('status')
        if request.GET.get('date_from'):
            filters['date_from'] = request.GET.get('date_from')
        if request.GET.get('date_to'):
            filters['date_to'] = request.GET.get('date_to')

        logger.info(f"Applied filters: {filters}")

        try:
            order_service = OrderService()
            orders = order_service.get_order_history(user_id, filters)
            logger.info(f"Retrieved {orders.count()} orders")
        except Exception as e:
            logger.error(f"Service error: {str(e)}")
            raise ValidationError(f"Failed to retrieve orders: {str(e)}")

        try:
            if 'OrderSerializer' in globals():
                serializer = OrderSerializer(orders, many=True)
                orders_data = serializer.data
            else:
                orders_data = []
                for order in orders:
                    order_dict = {
                        'id': order.id,
                        'order_number': order.order_number,
                        'status': order.status,
                        'total_amount': str(order.total_amount),
                        'created_at': order.created_at.isoformat(),
                        'updated_at': order.updated_at.isoformat(),
                    }
                    orders_data.append(order_dict)
                logger.warning("Using fallback serialization - check serializers import")

            return Response({
                'orders': orders_data,
                'count': orders.count()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Serialization error: {str(e)}")
            raise ValidationError(f"Failed to serialize orders: {str(e)}")

    except AuthenticationFailed as e:
        logger.error(f"Authentication failed: {str(e)}")
        return Response({
            'error': 'Authentication failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return Response({
            'error': 'Validation error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Unexpected error in get_order_history - Type: {type(e).__name__}, Message: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return Response({
            'error': 'Internal server error',
            'message': f'Debug: {str(e)}' if DEBUG else 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_order_detail(request, pk):

    try:
        user_data = authenticate_user(request)
        user_id = user_data.get('user_id')

        order = Order.objects.get(id=pk)

        if order.user_id != user_id:
            return Response({
                'error': 'Permission denied',
                'message': 'You are not allowed to view this order'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except AuthenticationFailed as e:
        return Response({
            'error': 'Authentication failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

    except Order.DoesNotExist:
        return Response({
            'error': 'Not Found',
            'message': f'No order with id {pk} found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Unexpected error in get_order_detail: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([AllowAny])
def cancel_order(request, order_number):

    try:
        user_data = authenticate_user(request)
        user_id = user_data.get('user_id')

        order_service = OrderService()
        order = order_service.cancel_order(order_number, user_id)

        serializer = OrderSerializer(order)
        return Response({
            'message': 'Order cancelled successfully',
            'order': serializer.data
        }, status=status.HTTP_200_OK)

    except AuthenticationFailed as e:
        return Response({
            'error': 'Authentication failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

    except ValidationError as e:
        return Response({
            'error': 'Validation error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    except (NotFound, PermissionDenied) as e:
        return Response({
            'error': 'Order not found',
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Unexpected error in cancel_order: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def track_order(request, pk):
    user = authenticate_user(request)
    order = get_object_or_404(Order, pk=pk)
    if order.user_id != user['user_id']:
        return Response({'error': 'Forbidden'}, status=403)

    tracking = getattr(order, 'tracking', None)
    status_history = order.status_history.all().order_by('-created_at')

    return Response({
        'order_id': order.id,
        'current_status': order.status,
        'tracking_info': OrderTrackingSerializer(tracking).data if tracking else None,
        'status_history': OrderStatusHistorySerializer(status_history, many=True).data
    }, status=200)


# Admin-only views
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_order_status(request, pk):

    try:
        user_data = authenticate_user(request)
        user_id = user_data.get('user_id')

        order = get_object_or_404(Order, pk=pk)

        if order.user_id != user_id:
            return Response({
                'error': 'Permission denied',
                'message': 'You may only update your own orders'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderUpdateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService().update_order_status(
            order_number=order.order_number,
            new_status=serializer.validated_data['status'],
            admin_user_id=user_id,  # now any user
            tracking_data=serializer.validated_data.get('tracking_data'),
            notes=serializer.validated_data.get('notes')
        )

        return Response({
            'message': 'Order status updated successfully',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_200_OK)

    except AuthenticationFailed as e:
        return Response({
            'error': 'Authentication failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

    except ValidationError as e:
        return Response({
            'error': 'Validation error',
            'message': e.detail if hasattr(e, 'detail') else str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    except NotFound as e:
        return Response({
            'error': 'Order not found',
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Unexpected error in update_order_status: {str(e)}", exc_info=True)
        return Response({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_orders(request):

    try:
        user_data = authenticate_user(request)

        if not user_data.get('is_staff', False):
            return Response({
                'error': 'Permission denied',
                'message': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)

        queryset = Order.objects.all()

        if request.GET.get('status'):
            queryset = queryset.filter(status=request.GET.get('status'))
        if request.GET.get('user_id'):
            queryset = queryset.filter(user_id=request.GET.get('user_id'))
        if request.GET.get('date_from'):
            queryset = queryset.filter(created_at__gte=request.GET.get('date_from'))
        if request.GET.get('date_to'):
            queryset = queryset.filter(created_at__lte=request.GET.get('date_to'))

        page_size = int(request.GET.get('page_size', 20))
        page = int(request.GET.get('page', 1))
        start = (page - 1) * page_size
        end = start + page_size

        orders = queryset.order_by('-created_at')[start:end]
        total_count = queryset.count()

        serializer = OrderSerializer(orders, many=True)
        return Response({
            'orders': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        }, status=status.HTTP_200_OK)

    except AuthenticationFailed as e:
        return Response({
            'error': 'Authentication failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        logger.error(f"Unexpected error in get_all_orders: {str(e)}")
        return Response({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):

    return Response({
        'status': 'healthy',
        'service': 'order-service',
        'timestamp': timezone.now()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def debug_auth(request):

    try:
        user_data = authenticate_user(request)
        return Response({
            'status': 'success',
            'user_data': user_data,
            'message': 'Authentication successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e),
            'type': type(e).__name__
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_order(request, pk):

    user = authenticate_user(request)
    order = get_object_or_404(Order, pk=pk, user_id=user['user_id'])
    updated = OrderService().update_order_status(
        order_number=order.order_number,
        new_status='confirmed',
        admin_user_id=user['user_id']
    )
    return Response(OrderSerializer(updated).data, status=200)
