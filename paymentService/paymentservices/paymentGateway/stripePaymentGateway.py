import stripe

from paymentService import settings
from paymentservices.paymentGateway.paymentGateway import PaymentGateway


class StripePaymentGateway(PaymentGateway):
    def __init__(self):
        self.stripe_key = settings.STRIPE_SECRET_KEY
        self.stripe_webhook_key = settings.STRIPE_WEBHOOK_SECRET_KEY

    def create_payment_link(self, amount, user_name, user_email, user_mobile, order_id):
        stripe.api_key = self.stripe_key

        product = stripe.Product.create(
            name="Scaler Academy Course",
            description="(created by Stripe Shell)",
            active=True
        )
        # Create the price
        price_obj = stripe.Price.create(
            unit_amount=amount,
            currency="INR",
            product=product.id,
        )

        try:
            payment_link = stripe.PaymentLink.create(
                line_items=[{'price': price_obj.id, 'quantity': 1}],
                after_completion={
                    "type": "redirect",
                    "redirect": {
                        "url": "https://scaler.com"
                    }
                },
                invoice_creation={"enabled": True},
                phone_number_collection={"enabled": False}
            )
            return payment_link.url

        except Exception as e:
            # Handle errors (e.g., connection issues, invalid parameters)
            print(f"Error: {e}")
            raise Exception("Error creating payment link")
