from enum import Enum


class PaymentGatewayType(Enum):
    STRIPE = 'STRIPE'
    RAZORPAY = 'RAZORPAY'
    PAYPAL = 'PAYPAL'
    JUSPAY = 'JUSPAY'
