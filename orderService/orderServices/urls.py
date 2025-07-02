from django.urls import path

from orderServices.views.views import create_order, health_check, get_order_history, get_order_detail, cancel_order, \
    track_order, update_order_status, get_all_orders, debug_auth, confirm_order

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),
    path('debug/auth/', debug_auth, name='debug_auth'),

    # Customer order endpoints
    path('orders/', create_order, name='create_order'),
    path('orders/history/', get_order_history, name='get_order_history'),
    path('orders/<int:pk>/', get_order_detail, name='get_order_detail'),
    path('orders/<int:pk>/cancel/', cancel_order, name='cancel_order'),
    path('orders/<int:pk>/track/', track_order, name='track_order'),
    path('orders/<int:pk>/confirm/',confirm_order,name='confirm_orders'),
    # Admin endpoints
    path('orders/<int:pk>/status/', update_order_status, name='update_order_status'),
    path('admin/orders/', get_all_orders, name='get_all_orders'),
]
