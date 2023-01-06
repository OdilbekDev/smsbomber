import requests

url = 'https://api.express24.uz/client/v4/authentication/code'

my_phone = {'phone': '998997821703'}

response = requests.post(url, json = my_phone)
print(response.status_code)

for i in range(1, 100):
    response = requests.post(url, json = my_phone)