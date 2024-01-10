import requests

response = requests.get('https://www.google.com/', proxies={'http': '127.0.0.1:33210', 'https': '127.0.0.1:33210'})
print(response.status_code)
