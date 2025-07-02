import httpx

from api.services.product_service import get_product
import requests

def add_to_cart(user_id, product_id, quantity, token):
    product_data = get_product(product_id, token)

    if not product_data:
        raise Exception("Product not found.")

    item = {
        "product_id": product_id,
        "title": product_data["title"],
        "price": product_data["price"],
        "quantity": quantity
    }

    body = {
        "user_id": user_id,
        "items": [item]
    }

    response = httpx.post(
        "http://localhost:8003/api/cart/add/",
        json=body,
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 201:
        return response.json()

    raise Exception(f"Failed to add to cart. Status: {response.status_code}, Response: {response.text}")

def get_user_cart(token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get("http://localhost:8003/api/cart/", headers=headers)  # Use actual cart service URL
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception("Failed to retrieve cart: " + str(e))