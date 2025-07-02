import httpx

def get_product(product_id, token):
    response = httpx.get(
        f"http://localhost:8002/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise Exception("Product not found.")
    raise Exception("Product not found.")
