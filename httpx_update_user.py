import httpx
from Tools.Fakers import random_email

create_users_payload = {
  "email": random_email(),
  "password": "string",
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}
create_users_response = httpx.post("http://localhost:8000/api/v1/users", json=create_users_payload)
create_users_response_data = create_users_response.json()
print("Create users: ", create_users_response_data)

login_payload = {
    "email": create_users_payload["email"],
    "password": create_users_payload["password"]
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print("Login response: ", login_response_data)

patch_payload = {
  "email": random_email(),
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}

patch_users_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}
patch_response = httpx.patch(
    f"http://localhost:8000/api/v1/users/{create_users_response_data['user']['id']}", headers=patch_users_headers,json=patch_payload
)
print("Patch response: ", patch_response.status_code, patch_response.json())
