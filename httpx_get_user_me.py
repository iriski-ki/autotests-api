import httpx

payload = {
  "email": "user1@example.com",
  "password": "1111"
}
response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=payload)
print(response.status_code)
print(response.json())

token = response.json()["token"]["refreshToken"]

response = httpx.get("http://localhost:8000/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
print(response.status_code)
print(response.json())