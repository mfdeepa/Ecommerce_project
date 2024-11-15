import httpx
import injector


# class UserAdapter:
#     user_url = "http://localhost:8050/auth/login"
#
#     # @injector.Inject
#     def __init__(self):
#         self.client = httpx.Client()
#
#     def get_role_by_user(self, email, token) -> list:
#         response = self.client.post(self.user_url)
#         # response = response.json()
#         if response.status_code != 200:
#             return {"error": f"user is not valid: {response.status_code}"}
#         try:
#             data = response.json()
#             if data.get("user", {}).get("email") == email:
#                 data_role = data["user"].get("roles", [])
#                 return list(data_role)
#             else:
#                 return {"error": f"email and token not valid: {response.status_code}"}
#         except Exception as e:
#             return {"error": f"user is not valid: {e}"}

class UserAdapter:
    def __init__(self):
        self.client = httpx.Client()
        self.user_url = "http://localhost:8050/auth/validate"  # Change to your verification endpoint

    @classmethod
    def get_role_by_user(cls, email, token) -> list:
        adapter = cls()
        headers = {
            "Authorization": f"Bearer {token}",
            "X-User-Email": email
        }

        try:
            response = adapter.client.post(
                adapter.user_url,
                headers=headers
            )

            if response.status_code != 200:
                print(f"Auth service error: {response.status_code}, {response.text}")
                return []

            data = response.json()
            if data.get("user", {}).get("email") == email:
                return data["user"].get("roles", [])
            return []

        except Exception as e:
            print(f"Error connecting to auth service: {str(e)}")
            return []
        finally:
            adapter.client.close()