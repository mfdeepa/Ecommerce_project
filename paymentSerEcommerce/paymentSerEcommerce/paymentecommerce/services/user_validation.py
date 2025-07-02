import httpx
from rest_framework.exceptions import AuthenticationFailed


class UserAuthValidator:
    @staticmethod
    def validate_token(token: str) -> dict:
        try:
            url = f"http://localhost:8001/auth/validate_token?token={token}"
            headers = {"Authorization": f"Bearer {token}"}
            response = httpx.get(url, headers=headers, timeout=5.0)
            # response = httpx.get(url, timeout=5.0)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthenticationFailed("Invalid or expired token.")
            else:
                raise AuthenticationFailed(f"User validation failed with status code {response.status_code}")
        except httpx.RequestError as e:
            raise AuthenticationFailed(f"Error connecting to user service: {str(e)}")
