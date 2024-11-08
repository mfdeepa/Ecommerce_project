from django.urls import path

from paymentservices.views.paymentView import PaymentServiceView

urlpatterns = [
    path("service/", PaymentServiceView.as_view(), name="payment_service"),
]