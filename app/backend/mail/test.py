import requests
res = requests.get('http://localhost:5000/api/ticket/submit', json=payload)

print(res)
