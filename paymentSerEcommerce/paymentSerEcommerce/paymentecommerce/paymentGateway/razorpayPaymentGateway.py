import json
import time
import razorpay

from paymentSerEcommerce import settings
from paymentecommerce.paymentGateway.paymentGateway import PaymentGateway


class RazorpayPaymentGateway(PaymentGateway):

    def __init__(self):
        super().__init__()
        self.client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))

    def create_payment_link(self, amount, user_name, user_email, user_mobile, order_id):

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "description": "For XYZ purpose",
            "accept_partial": False,
            "expire_by": int(time.time()) + 15 * 60,  # Expire in 15 minutes
            "reference_id": order_id,
            "customer": {
                "name": user_name,
                "email": user_email,
                "contact": user_mobile
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "notes": {
                "Order Items": "1. iPhone 15 Pro Max"
            },
            "callback_url": "https://google.com/",
            "callback_method": "get"
        }
        url = "https://google.com/" # this line is added, because I don't have a razor pay secret key and return same.

        # try:
        #     payment_link = self.client.payment_link.create(payment_data)
        #     return json.dumps(payment_link)
        # except Exception as e:
        #     print("Error creating payment link:", e)
        #     return url
        #     # return None
        return url
