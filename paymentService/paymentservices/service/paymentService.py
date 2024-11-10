from paymentservices.paymentGateway.paymentGatewayStrategy import PaymentGatewayStrategy
from paymentservices.paymentGateway.razorpayPaymentGateway import RazorpayPaymentGateway
from paymentservices.paymentGateway.stripePaymentGateway import StripePaymentGateway


class PaymentService:
    def __init__(self):
        self.payment_gateway_strategy = PaymentGatewayStrategy()
        # self.razorpay_payment_gateway = RazorpayPaymentGateway()
        # self.stripe_payment_gateway = StripePaymentGateway()

    def create_payment_link(self, order_id):
        amount = 10000000
        user_name = "Deepa"
        user_email = "mf.deepa.aggarwal@gmail.com"
        user_mobile = "123456789"

        payment_gateway = self.payment_gateway_strategy.get_payment_gateway()
        url = ""
        try:
            url = payment_gateway.create_payment_link(amount, user_name, user_email, user_mobile, order_id)
        except Exception as e:
            print(f"An error occurred: {e}")
        print("url:", url)
        return url


    # def get_payment_status(self, payment_gateway_payment_id):
    #     pass
    # String paymentLink = paymentGateway.createPaymentLink(
    #             amount, userName, userEmail, userMobile, orderId
    #     );