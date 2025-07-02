import httpx

def create_payment(order_id, token, user_name, user_email, user_mobile, total_amount):
    total_amount = str(total_amount)
    print(total_amount)

    url = "http://localhost:8010/payment/service/"

    response = httpx.post(
        url,
        json={
            "order_id": order_id,
            "total_amount": total_amount,
            "user_name": user_name,
            "user_email": user_email,
            "user_mobile": user_mobile
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code in [200, 201]:
        return response.json()

    raise Exception("Payment creation failed.")
