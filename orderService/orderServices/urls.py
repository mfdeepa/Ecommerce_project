from django.urls import path
from orderServices import views

urlpatterns = [
    # POST /api/orders/create/
    path('create/', views.CreateOrderView.as_view(), name='create-order'),

    # GET /api/orders/
    path('', views.OrderHistoryView.as_view(), name='order-history'),

    # GET /api/orders/<order_number>/
    path('<str:order_number>/', views.OrderDetailView.as_view(), name='order-detail'),

    # --- Order Actions ---
    # POST /api/orders/<order_number>/cancel/
    path('<str:order_number>/cancel/', views.cancel_order, name='cancel-order'),

    # POST /api/orders/<order_number>/update-status/ (Admin)
    path('<str:order_number>/update-status/', views.update_order_status, name='update-order-status'),
]
