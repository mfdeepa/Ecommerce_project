
import requests

def fetch_user_snapshot(user_id, token):
    url = f"http://localhost:8001/api/users/{user_id}/"  # adjust as per your user service
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return {
            "name": user_data.get("name"),
            "email": user_data.get("email")
        }
    return {}
