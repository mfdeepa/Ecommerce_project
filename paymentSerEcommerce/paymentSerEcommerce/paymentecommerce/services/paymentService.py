import stripe

from paymentecommerce.paymentGateway.paymentGatewayStrategy import PaymentGatewayStrategy


class PaymentService:
    def __init__(self):
        self.payment_gateway_strategy = PaymentGatewayStrategy()

    def create_payment_link(self, order_id, total_amount, user_name, user_email, user_mobile):

        payment_gateway = self.payment_gateway_strategy.get_payment_gateway()
        print("Payment Gateway is {}".format(payment_gateway))

        url = ""

        try:
            print("now sending data to payment gateway")
            url = payment_gateway.create_payment_link(total_amount, user_name, user_email, user_mobile, order_id)
            print("url in service: {}".format(url))

        except Exception as e:
            print(f"An error occurred: {e}")
        print("url after try catch block in service :", url)

        return url

