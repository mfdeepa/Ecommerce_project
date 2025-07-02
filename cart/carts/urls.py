from django.urls import path
from carts.view.cartView import CartViewSet
from carts.view.discountView import CartDiscountViewSet
from carts.view.productView import ProductViewSet

urlpatterns = [

    # Cart operations
    path('api/cart/', CartViewSet.as_view({'get': 'cart'}), name='cart-view'),
    path('api/cart/add/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add'),
    path('api/cart/update/<int:pk>/', CartViewSet.as_view({'post': 'update_quantity'}), name='cart-update'),
    path('api/cart/remove/<int:pk>/', CartViewSet.as_view({'delete': 'delete_item'}), name='cart-remove'),
    path('api/cart/clear/', CartViewSet.as_view({'post': 'clear_cart'}), name='cart-clear'),

    # Discount operations
    path('api/cart/apply-discount/', CartDiscountViewSet.as_view({'post': 'apply_discount'}), name='apply-discount'),

    # Product inventory check
    path('api/products/check-inventory/<int:product_id>/', ProductViewSet.as_view({'get': 'check_inventory'}), name='product-check-inventory'),
]
