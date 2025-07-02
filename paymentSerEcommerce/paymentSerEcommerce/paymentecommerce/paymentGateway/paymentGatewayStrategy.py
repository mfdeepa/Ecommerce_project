import random

from paymentecommerce.paymentGateway.razorpayPaymentGateway import RazorpayPaymentGateway
from paymentecommerce.paymentGateway.stripePaymentGateway import StripePaymentGateway


class PaymentGatewayStrategy:
    razorpay_payment_gateway = RazorpayPaymentGateway()
    stripe_payment_gateway = StripePaymentGateway()

    def get_payment_gateway(self):
        payment_list = ["RazorpayPayment", "StripePayment"]

        random_choice = random.choice(payment_list)
        url = "https://www.google.com/"
        if random_choice == "StripePayment":
            return self.stripe_payment_gateway
        return self.razorpay_payment_gateway
