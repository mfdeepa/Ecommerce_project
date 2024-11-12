from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts.view.cartView import CartViewSet
from carts.view.discountView import CartDiscountViewSet
from carts.view.productView import ProductViewSet

# router = DefaultRouter()
# router.register(r'carts', CartViewSet, basename='cart')
# router.register(r'products', ProductViewSet, basename='product')
# router.register(r'discounts', DiscountViewSet, basename='discount')

urlpatterns = [
    # path('api/', include(router.urls)),

    path('api/carts/get-item/<int:cart_id>', CartViewSet.as_view({'get': 'get_cart_details'}), name='cart-get-item'),

    path('api/carts/add-item/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),

    path('api/carts/bulk-add/', CartViewSet.as_view({'post': 'bulk_add_item'}), name='cart-bulk-add'),

    path('api/carts/update-quantity/<int:cart_id>/', CartViewSet.as_view({'post': 'update_quantity'}), name='cart-update-quantity'),

    path('api/carts/<int:cart_id>/apply-discount/', CartDiscountViewSet.as_view({'post': 'apply_discount'}), name='cart-apply-discount'),

    path('api/carts/<int:cart_id>/remove-item/', CartViewSet.as_view({'delete': 'delete_cart_item'}), name='cart-remove-item'),

    path('api/carts/<int:cart_id>/clear/', CartViewSet.as_view({'post': 'clear_cart'}), name='cart-clear'),

    path('api/products/check-inventory/<int:product_id>', ProductViewSet.as_view({'get': 'check_inventory'}), name='check-inventory'),
    # path('api/products/<int:pk>/check-inventory', ProductViewSet.as_view({'get': 'check_inventory'}), name='check-inventory'),


]