import time

from django.shortcuts import render



import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .config import WEBPAY_BASE_URL, WEBPAY_COMMERCE_CODE,  WEBPAY_API_KEY


from django.http import JsonResponse

"""
class TransbankService:
    def __init__(self):
        self.api_key = settings.TRANSBANK['API_KEY']
        self.commerce_code = settings.TRANSBANK['COMMERCE_CODE']
        self.environment = settings.TRANSBANK['ENVIRONMENT']
        self.base_url = 'https://webpay3g.transbank.cl'

    def create_transaction(self, buy_order, session_id, amount, return_url):
        url = f"{self.base_url}/rswebpaytransaction/api/webpay/v1.2/transactions"
        headers = {
            'Tbk-Api-Key-Id': self.commerce_code,
            'Tbk-Api-Key-Secret': self.api_key,
            'Content-Type': 'application/json',
        }
        payload = {
            'buy_order': buy_order,
            'session_id': session_id,
            'amount': amount,
            'return_url': return_url,
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def commit_transaction(self, token):
        url = f"{self.base_url}/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        headers = {
            'Tbk-Api-Key-Id': self.commerce_code,
            'Tbk-Api-Key-Secret': self.api_key,
            'Content-Type': 'application/json',
        }
        response = requests.put(url, headers=headers)
        return response.json()

"""


def create_transaction(request):
    total = request.session.get('total', 0)


    url = f"{WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.0/transactions"
    headers = {
        "Tbk-Api-Key-Id": WEBPAY_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": WEBPAY_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {

        "buy_order": "1",
        "session_id": "time.time()",
        "amount": total,
        "return_url": "http://127.0.0.1:8000/webpay/webpay/return/",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return render(request, 'webPay/redirecionamiento.html', {'url': data['url'], 'token': data['token']})
    else:
        return JsonResponse({'error': 'Error al crear la transacción'}, status=response.status_code)



@csrf_exempt
def return_from_webpay(request):

    token = request.POST.get('token_ws')
    if not token:
        return JsonResponse({'error': 'Token no encontrado'}, status=400)
    url = f"{WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.0/transactions/{token}"
    headers = {
        "Tbk-Api-Key-Id": WEBPAY_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": WEBPAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return render(request, 'webPay/correcto.html', {'data': data})
    else:
        error_message = f"Error al confirmar la transacción: {response.status_code} - {response.text}"
        print(error_message)  # Imprime el error en la consola para depuración
        return JsonResponse({'error': error_message}, status=response.status_code)





"""
def return_from_webpay(request):
    token = request.POST.get('token_ws')
    url = f"{WEBPAY_BASE_URL}/rswebpaytransaction/api/webpay/v1.0/transactions/{token}"
    headers = {
        "Tbk-Api-Key-Id": WEBPAY_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": WEBPAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return render(request, 'webPay/correcto.html', {'data': data})
    else:
        return JsonResponse({'error': 'Error al confirmar la transacción'}, status=response.status_code)


"""

