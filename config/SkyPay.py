import requests

url = "https://papi.skycrypto.net/rest/v2/payments_v2 "
data = {
    "amount": 500,  # Сумма
    "symbol": "usdt",  # Валюта
    "currency": "rub",  #
    "is_currency_amount": True,
    "broker_id": "efdsghnm,jmhngbfd"
}
response = requests.post(url, json=data, headers={'Authorization': 'Token ae83897f7ad94aaeb0e31330932d6c7c'})
print(response.json())
