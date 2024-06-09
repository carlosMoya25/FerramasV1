"""def cart_total_amount(request):
    total = 0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            total += float(value['price']) * value['quantity']
    return {'cart_total_amount': total}
"""
from datetime import datetime
import requests

def obtener_valor_dolar():
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    params = {
        'user': 'ca.moyar@duocuc.cl',
        'pass': 'Ca18091998.',
        'function': 'GetSeries',
        'timeseries': 'F073.TCO.PRE.Z.D',
        'firstdate': hoy,
        'lastdate': hoy
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        datos = response.json()
        if datos['Series']['Obs']:
            return float(datos['Series']['Obs'][0]['value'])
    return None

def cart_total_amount(request):
    total = 0

    cart = request.session.get('cart', {})
    for key, value in cart.items():
        total += float(value['price']) * value['quantity']
    return {'cart_total_amount': total}


def cart_total_amount_dolar(request):
    valor_dolar = obtener_valor_dolar()
    if valor_dolar is None:
        valor_dolar =1
    total_dolar = 0

    cart = request.session.get('cart', {})
    for key, value in cart.items():
        total_dolar += (float(value['price']) * value['quantity']) / valor_dolar
    return {'cart_total_amount_dolar': total_dolar}



