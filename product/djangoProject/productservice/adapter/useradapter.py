import httpx


class UserAdapter:
    user_url = "http://localhost:8050/auth/validate"

    def __init__(self):
        self.client = httpx.Client()

    def get_role_by_user(self, email, token) -> list:
        print("validating email and token")
        response = self.client.post(self.user_url, json={"email": email, "token": token})
        print(response)

        if response.status_code != 200:
            return {"error": f"user is not valid: {response.status_code}"}
        try:
            data = response.json()
            if data.get("user", {}).get("email") == email:
                data_role = data["user"].get("roles", [])
                return list(data_role)
            else:
                return {"error": f"email and token not valid: {response.status_code}"}
        except Exception as e:
            return {"error": f"user is not valid: {e}"}
