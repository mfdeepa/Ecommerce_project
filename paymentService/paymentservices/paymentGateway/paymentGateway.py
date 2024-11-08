from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def create_payment_link(self, price):
        pass

    # @abstractmethod
    # def get_payment_status(self, payment_id):
    #     pass
