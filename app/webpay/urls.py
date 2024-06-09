# payments/urls.py

from django.urls import path

#from orders.views import create_transaccion, return_from_transbank

from .views import create_transaction, return_from_webpay


urlpatterns = [

    path('webpay/create/', create_transaction, name='create_transaction'),
    path('webpay/return/', return_from_webpay, name='return_from_webpay'),
]
