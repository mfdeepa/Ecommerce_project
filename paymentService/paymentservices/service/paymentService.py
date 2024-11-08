from paymentservices.paymentGateway.paymentGatewayStrategy import PaymentGatewayStrategy
from paymentservices.paymentGateway.razorpayPaymentGateway import RazorpayPaymentGateway
from paymentservices.paymentGateway.stripePaymentGateway import StripePaymentGateway


class PaymentService:
    def __init__(self):
        self.payment_gateway_strategy = PaymentGatewayStrategy()
        # self.razorpay_payment_gateway = RazorpayPaymentGateway()
        # self.stripe_payment_gateway = StripePaymentGateway()

    def create_payment_link(self, order_id):
        price = 10000000
        payment_gateway = self.payment_gateway_strategy.get_payment_gateway()
        url = ""
        try:
            url = payment_gateway.create_payment_link(price)
        except Exception as e:
            print(f"An error occurred: {e}")
        print("url:", url)
        return url


    # def get_payment_status(self, payment_gateway_payment_id):
    #     pass
