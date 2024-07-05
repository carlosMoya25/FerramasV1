from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
#from .models import Product
# Create your views here.
from cart.cart import Cart

@login_required(login_url='/autenticacion/acceder')
def cajero (request):
    cart = Cart(request)
    products = Product.objects.all()
    return render(request,"Cajero/cajero.html", {
        "products": products

    })