from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import webpay.urls

from bnCentral.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacion/', include('autenticacion.urls')),
    path('productos/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('webpay/', include('webpay.urls')),
    path('inicio/', inicio, name='inicio'),
    path('api/', include('ConsumoApi.urls')),
    path('cajero/', include('cajero.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
