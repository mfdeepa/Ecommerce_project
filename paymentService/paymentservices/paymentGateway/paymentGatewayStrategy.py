import random

from paymentservices.models.paymentGatewayType import PaymentGatewayType
from paymentservices.paymentGateway.razorpayPaymentGateway import RazorpayPaymentGateway
from paymentservices.paymentGateway.stripePaymentGateway import StripePaymentGateway


class PaymentGatewayStrategy:
    razorpay_payment_gateway = RazorpayPaymentGateway()
    stripe_payment_gateway = StripePaymentGateway()

    def get_payment_gateway(self):
        payment_list = ["RazorpayPayment", "StripePayment"]

        # # Randomly selecting a payment gateway
        random_choice = random.choice(payment_list)

        if random_choice == "StripePayment":
            return self.stripe_payment_gateway
        return self.razorpay_payment_gateway
