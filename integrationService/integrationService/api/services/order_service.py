import requests

import json


def place_order(user_id, token, cart_data, shipping_address, billing_address, payment_method):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        clean_items = [
            {
                "product_id": item["product_id"],
                "title": item["title"],
                "price": item["price"],
                "quantity": item["quantity"]
            }
            for item in cart_data["items"]
        ]

        payload = {
            "shipping_address": shipping_address,
            "billing_address": billing_address,
            "payment_method": payment_method,
            "items": clean_items
        }

        response = requests.post("http://localhost:8004/api/orders/", json=payload, headers=headers)

        try:
            response.raise_for_status()
        except requests.HTTPError:
            print("Error from Order Service:")
            print(response.text)
            raise

        return response.json()

    except requests.RequestException as e:
        raise Exception("Failed to place order: " + str(e))


def get_user_order(token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get("http://localhost:8004/api/orders/history/", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception("Failed to retrieve cart: " + str(e))
