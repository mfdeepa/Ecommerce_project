from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service_caller import ServiceCaller

service_caller = ServiceCaller()


class AddToCartIntegrationView(APIView):
    """
    Frontend calls this endpoint
    This service then calls: User → Product → Cart
    """

    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        print(f"Step 1: Validating user {user_id}")

        # STEP 1: Call User Service first
        user_result = service_caller.call_user_service(f'users/{user_id}/')
        if not user_result['success']:
            return Response({'error': 'User not found'}, status=400)

        print(f"Step 2: Validating product {product_id}")

        # STEP 2: Call Product Service second
        product_result = service_caller.call_product_service(f'products/{product_id}/')
        if not product_result['success']:
            return Response({'error': 'Product not found'}, status=400)

        product_data = product_result['data']
        if product_data.get('stock', 0) < quantity:
            return Response({'error': 'Not enough stock'}, status=400)

        print(f"Step 3: Adding to cart")

        # STEP 3: Call Cart Service third
        cart_data = {
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'price': product_data['price']
        }

        cart_result = service_caller.call_cart_service('cart/add/', 'POST', cart_data)
        if not cart_result['success']:
            return Response({'error': 'Failed to add to cart'}, status=400)

        return Response({
            'message': 'Item added to cart successfully',
            'user': user_result['data']['name'],
            'product': product_data['name'],
            'quantity': quantity,
            'cart_data': cart_result['data']
        })


class PlaceOrderIntegrationView(APIView):
    """
    Complete order flow
    Calls: User → Cart → Product → Payment → Order
    """

    def post(self, request):
        user_id = request.data.get('user_id')
        payment_method = request.data.get('payment_method', 'card')

        print(f"=== Starting Order Process for User {user_id} ===")

        # STEP 1: Validate User
        print("Step 1: Validating user...")
        user_result = service_caller.call_user_service(f'users/{user_id}/')
        if not user_result['success']:
            return Response({'error': 'User not found'}, status=400)

        # STEP 2: Get Cart Items
        print("Step 2: Getting cart items...")
        cart_result = service_caller.call_cart_service(f'cart/user/{user_id}/')
        if not cart_result['success'] or not cart_result['data'].get('items'):
            return Response({'error': 'Cart is empty'}, status=400)

        cart_items = cart_result['data']['items']
        total_amount = 0

        # STEP 3: Validate Products and Calculate Total
        print("Step 3: Validating products...")
        for item in cart_items:
            product_result = service_caller.call_product_service(f'products/{item["product_id"]}/')
            if not product_result['success']:
                return Response({'error': f'Product {item["product_id"]} not found'}, status=400)

            product = product_result['data']
            if product.get('stock', 0) < item['quantity']:
                return Response({'error': f'Not enough stock for {product["name"]}'}, status=400)

            total_amount += product['price'] * item['quantity']

        # STEP 4: Process Payment
        print("Step 4: Processing payment...")
        payment_data = {
            'user_id': user_id,
            'amount': total_amount,
            'payment_method': payment_method
        }

        payment_result = service_caller.call_payment_service('payment/process/', 'POST', payment_data)
        if not payment_result['success']:
            return Response({'error': 'Payment failed'}, status=400)

        # STEP 5: Create Order
        print("Step 5: Creating order...")
        order_data = {
            'user_id': user_id,
            'items': cart_items,
            'total_amount': total_amount,
            'payment_id': payment_result['data']['payment_id']
        }

        order_result = service_caller.call_order_service('orders/create/', 'POST', order_data)
        if not order_result['success']:
            return Response({'error': 'Order creation failed'}, status=400)

        print("Step 6: Updating product stock...")
        # STEP 6: Update Product Stock
        for item in cart_items:
            stock_data = {'quantity': item['quantity']}
            service_caller.call_product_service(f'products/{item["product_id"]}/reduce-stock/', 'POST', stock_data)

        print("Step 7: Clearing cart...")
        # STEP 7: Clear Cart
        service_caller.call_cart_service(f'cart/user/{user_id}/clear/', 'DELETE')

        print("=== Order Process Complete ===")

        return Response({
            'message': 'Order placed successfully!',
            'order_id': order_result['data']['order_id'],
            'payment_id': payment_result['data']['payment_id'],
            'total_amount': total_amount,
            'user': user_result['data']['name']
        })


class GetUserCartView(APIView):
    """
    Get user cart with product details
    Calls: User → Cart → Product (for each item)
    """

    def get(self, request, user_id):
        print(f"Getting cart for user {user_id}")

        # STEP 1: Validate User
        user_result = service_caller.call_user_service(f'users/{user_id}/')
        if not user_result['success']:
            return Response({'error': 'User not found'}, status=400)

        # STEP 2: Get Cart
        cart_result = service_caller.call_cart_service(f'cart/user/{user_id}/')
        if not cart_result['success']:
            return Response({'cart_items': [], 'total': 0})

        cart_items = cart_result['data'].get('items', [])
        enriched_items = []
        total_amount = 0

        # STEP 3: Get Product Details for each item
        for item in cart_items:
            product_result = service_caller.call_product_service(f'products/{item["product_id"]}/')
            if product_result['success']:
                product = product_result['data']
                item_total = product['price'] * item['quantity']
                total_amount += item_total

                enriched_items.append({
                    'product_id': item['product_id'],
                    'product_name': product['name'],
                    'product_image': product.get('image_url', ''),
                    'price': product['price'],
                    'quantity': item['quantity'],
                    'item_total': item_total,
                    'stock_available': product.get('stock', 0)
                })

        return Response({
            'user_name': user_result['data']['name'],
            'cart_items': enriched_items,
            'total_amount': total_amount,
            'total_items': len(enriched_items)
        })


class GetOrderHistoryView(APIView):
    """
    Get user order history with details
    Calls: User → Order → Product (for each order item)
    """

    def get(self, request, user_id):
        # STEP 1: Validate User
        user_result = service_caller.call_user_service(f'users/{user_id}/')
        if not user_result['success']:
            return Response({'error': 'User not found'}, status=400)

        # STEP 2: Get Orders
        orders_result = service_caller.call_order_service(f'orders/user/{user_id}/')
        if not orders_result['success']:
            return Response({'orders': []})

        orders = orders_result['data']
        enriched_orders = []

        # STEP 3: Enrich each order with product details
        for order in orders:
            order_items = []
            for item in order.get('items', []):
                product_result = service_caller.call_product_service(f'products/{item["product_id"]}/')
                if product_result['success']:
                    product = product_result['data']
                    order_items.append({
                        'product_name': product['name'],
                        'quantity': item['quantity'],
                        'price': item['price']
                    })

            enriched_orders.append({
                'order_id': order['order_id'],
                'order_date': order['created_at'],
                'total_amount': order['total_amount'],
                'status': order['status'],
                'items': order_items
            })

        return Response({
            'user_name': user_result['data']['name'],
            'orders': enriched_orders
        })
