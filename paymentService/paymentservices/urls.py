from django.urls import path

from paymentservices.views.paymentView import PaymentServiceView, StripeWebhookView

urlpatterns = [
    path("service/", PaymentServiceView.as_view(), name="payment_service"),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),

]