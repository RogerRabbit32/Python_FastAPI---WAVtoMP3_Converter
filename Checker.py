import requests

url = "http://localhost:8000/record"
body = {
    "user_id": 12345,
    "user_access_token": "test_token",
    "audio": open(r"C:\Users\79523\Desktop\Альбом\Diamonds.wav", "rb")
}

response = requests.post(url, files=body)
print(response.json())
