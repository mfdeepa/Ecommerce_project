import httpx

def validate_token(token):
    response = httpx.get(
        f"http://localhost:8001/auth/validate_token?token={token}",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        return response.json()  # user info
    raise Exception("Invalid or expired token.")
