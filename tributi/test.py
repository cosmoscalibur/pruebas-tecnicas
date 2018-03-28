import requests
token = "AQUÍ VA EL TOKEN"
r = requests.post("http://127.0.0.1:5000/user", data={"token": token})
print(r.json())

r = requests.get("http://127.0.0.1:5000/user", params={"token": token})
print(r.json())
