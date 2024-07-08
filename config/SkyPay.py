import requests
import asyncio


async def createInvoice(sum):  # Метод создания платежа
    url = "https://papi.skycrypto.net/rest/v2/purchases"
    data = {
        "amount": sum,  # Сумма
        "symbol": "usdt",  # Валюта
        "currency": "rub",  #
        "is_currency_amount": True,
    }
    response = requests.post(url, json=data, headers={'Authorization': 'Token ae83897f7ad94aaeb0e31330932d6c7c'})
    print(response.json())
    return response.json()['web_link'], response.json()['payment_id']


async def checkPayment(payment_id):  # Метод проверки оплаты
    url = f"https://papi.skycrypto.net/rest/v2/purchases/{str(payment_id)}"

    response = requests.get(url, headers={'Authorization': 'Token ae83897f7ad94aaeb0e31330932d6c7c'})
    print(response.json())


async def main():
    status = await checkPayment("")  # Проверка статуса платежа


if __name__ == '__main__':
    asyncio.run(main())
