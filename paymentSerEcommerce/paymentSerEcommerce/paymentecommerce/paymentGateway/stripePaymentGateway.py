from decimal import Decimal
import stripe
from django.conf import settings
from paymentecommerce.paymentGateway.paymentGateway import PaymentGateway


class StripePaymentGateway(PaymentGateway):
    def __init__(self):
        self.stripe_key = settings.STRIPE_SECRET_KEY
        self.stripe_webhook_key = settings.STRIPE_WEBHOOK_SECRET_KEY

        if not self.stripe_key:
            raise ValueError("Missing Stripe secret key")

        stripe.api_key = self.stripe_key

    def create_payment_link(self, total_amount, user_name, user_email, user_mobile, order_id):
        total_amount = int(Decimal(str(total_amount)) * 100)

        try:
            product = stripe.Product.create(
                name=f"Order #{order_id}",
                description="Scaler course payment"
            )
        except Exception as e:
            raise  # Let it bubble up to Django for full traceback

        try:
            price_obj = stripe.Price.create(
                unit_amount=total_amount,
                currency="INR",
                product=product.id,
            )
        except Exception as e:
            raise

        try:
            payment_link = stripe.PaymentLink.create(
                line_items=[{"price": price_obj.id, "quantity": 1}],
                after_completion={
                    "type": "redirect",
                    "redirect": {
                        "url": "https://scaler.com"
                    }
                },
                invoice_creation={"enabled": True}
            )
            return payment_link.url
        except Exception as e:
            raise
