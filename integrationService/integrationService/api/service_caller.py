import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ServiceCaller:
    def __init__(self):
        self.services = settings.MICROSERVICES

    def call_user_service(self, endpoint, method='GET', data=None):
        """Call User Service"""
        url = f"{self.services['USER_SERVICE']}/api/{endpoint}"
        return self._make_request(url, method, data)

    def call_product_service(self, endpoint, method='GET', data=None):
        """Call Product Service"""
        url = f"{self.services['PRODUCT_SERVICE']}/api/{endpoint}"
        return self._make_request(url, method, data)

    def call_cart_service(self, endpoint, method='GET', data=None):
        """Call Cart Service"""
        url = f"{self.services['CART_SERVICE']}/api/{endpoint}"
        return self._make_request(url, method, data)

    def call_order_service(self, endpoint, method='GET', data=None):
        """Call Order Service"""
        url = f"{self.services['ORDER_SERVICE']}/api/{endpoint}"
        return self._make_request(url, method, data)

    def call_payment_service(self, endpoint, method='GET', data=None):
        """Call Payment Service"""
        url = f"{self.services['PAYMENT_SERVICE']}/api/{endpoint}"
        return self._make_request(url, method, data)

    def _make_request(self, url, method='GET', data=None):
        """Make HTTP request to any service"""
        try:
            if method == 'GET':
                response = requests.get(url, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=30)

            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': f'Status: {response.status_code}'}

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed to {url}: {str(e)}")
            return {'success': False, 'error': str(e)}