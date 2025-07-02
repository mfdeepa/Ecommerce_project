from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def create_payment_link(self, amount, user_name, user_email, user_mobile, order_id):
        pass
