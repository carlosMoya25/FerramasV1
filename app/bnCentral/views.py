from django.shortcuts import render

# currency_converter/views.py

from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime


def inicio(request):
    valor_dolar = obtener_valor_dolar()
    request.session['valor_dolar'] = valor_dolar

    return render(request, 'bancoCentral/convertidor.html', {'valor_dolar': valor_dolar})



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
    datos = response.json()
    if datos['Series']['Obs']:
        return datos['Series']['Obs'][0]['value']
    else:
        return "Datos no disponibles"



"""
def inicio(request):
    valor_dolar = obtener_valor_dolar()
    if valor_dolar is None:
        valor_dolar = 1  # Valor de respaldo si no se puede obtener el valor del dólar

    # Obtener productos del carrito desde la sesión
    productos = request.session.get('cart', {}).get('items', {})

    # Calcular el total en CLP y en USD para cada producto
    total_clp = 0
    for key, value in productos.items():
        total_clp += value['price'] * value['quantity']

    total_usd = total_clp / valor_dolar if valor_dolar != 1 else "Datos no disponibles"

    return render(request, 'bancoCentral/convertidor.html', {
        'valor_dolar': valor_dolar,
        'total_clp': total_clp,
        'total_usd': total_usd,
        'productos': productos,
    })


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



"""







"""
from django.shortcuts import render
import requests
from datetime import datetime


def inicio(request):
    valor_dolar = obtener_valor_dolar()
    # Suponiendo que request.session.cart.items contiene los productos en el carrito
    productos = request.session.get('cart', {}).get('items', {})

    # Calcular el total en CLP y en USD para cada producto
    total_clp = 0
    productos_en_dolares = []
    for key, value in productos.items():
        precio_total_clp = value['price'] * value['quantity']
        precio_total_usd = precio_total_clp / valor_dolar
        total_clp += precio_total_clp
        productos_en_dolares.append({
            'name': value['name'],
            'quantity': value['quantity'],
            'price_clp': value['price'],
            'price_usd': precio_total_usd,
        })

    total_usd = total_clp / valor_dolar
    return render(request, 'bancoCentral/convertidor.html', {
        'valor_dolar': valor_dolar,
        'productos_en_dolares': productos_en_dolares,
        'total_clp': total_clp,
        'total_usd': total_usd,
    })


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
    datos = response.json()
    if datos['Series']['Obs']:
        return float(datos['Series']['Obs'][0]['value'])
    else:
        return None
"""