Installation

Install the package

$ pip install django-payments

Most providers have additional dependencies. For example, if using stripe, you should run:
$ pip install "django-payments[stripe]"

Multiple providers can be specified comma-separated, e.g.:
$ pip install "django-payments[mercadopago,stripe]"

Configure Django

payments needs to be registered as a Django app by adding it to settings.py:

INSTALLED_APPS = [
  ...
  "payments",
  "rest_framework"
  ...
]
There is no strong requirement for it to be listed first nor last.

Add the callback processor to your URL router (urls.py).

# urls.py
from django.conf.urls import include, path

urlpatterns = [
    path('payments/', include('payments.urls')),
]
This includes two sets of URLs:

Views (endpoints) where notifications will be received from payment providers. These must be exposed properly for the provider to notify us of any payment. Note that these notifications may be delivered _after_ the user has navigated away from the website.
Views where users are directed after completing a payment. Usually, once the user has completed a flow at the payment provider's website, their browser will be redirected to one of these views and POST some additional data. These views parse this data, communicate with the provider (if a necessary) and then redirect the user to a view of your choosing.
None of these views render any "pages" that your users might every see.

for download strip install -> pip install stripe
for download razopay install -> pip install razorpay

After download, configure in setting.py
# Razorpay configuration
RAZORPAY_KEY_ID = 'your_razorpay_key_id'
RAZORPAY_KEY_SECRET = 'your_razorpay_key_secret'

# Stripe configuration
STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
STRIPE_SECRET_KEY = 'your_stripe_secret_key'

and add in payment_variant
PAYMENT_VARIANTS = {
    'razorpay': {
        'provider': 'razorpay',
        'key_id': RAZORPAY_KEY_ID,
        'key_secret': RAZORPAY_KEY_SECRET,
    },
    'stripe': {
        'provider': 'stripe',
        'public_key': STRIPE_PUBLIC_KEY,
        'secret_key': STRIPE_SECRET_KEY,
    }
}

2. install rest framework -> pip install djangorestframework
    and add the application into INSTALLED_APPS["rest_framework"]

 => Razor pay Gateway
    1. Install razorpay -> pip install razorpay
    2. In setting write id and secret

=> to download pkg_resources -> install setuptools -> commend is pip install setuptools

