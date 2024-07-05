from django.urls import path
from .views import  cajero

urlpatterns = [
    
    path('', cajero, name='cajero'),

]
