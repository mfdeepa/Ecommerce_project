from django.urls import path
from . import views
from django.urls import path

from .views.cart import AddToCartView
from .views.order import PlaceOrderView
from .views.payment import PaymentInitiateView

urlpatterns = [
    path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
    path("orders/place/", PlaceOrderView.as_view(), name="place_order"),
    path("payment/initiate/", PaymentInitiateView.as_view(), name="initiate_payment"),
]
