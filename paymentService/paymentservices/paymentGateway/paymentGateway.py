from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    # @abstractmethod
    # def create_payment_link(self, price):
    #     pass

    @abstractmethod
    def create_payment_link(self, amount, user_name, user_email, user_mobile, order_id):
        pass
    # @abstractmethod
    # def get_payment_status(self, payment_id):
    #     pass
    # String paymentLink = paymentGateway.createPaymentLink(
    #             amount, userName, userEmail, userMobile, orderId
    #     );