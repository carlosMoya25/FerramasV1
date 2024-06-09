from django.urls import path
from .views import listado_productos

urlpatterns = [
    path('', listado_productos, name='listado_productos')
]
