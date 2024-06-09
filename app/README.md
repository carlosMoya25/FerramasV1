# Very basic Ecommerce site with Django

### Partimos de un proyecto con autenticación básico

Instalar las siguientes dependencias
```shell
Django==3.1
django-crispy-forms==1.9.2
freeze==3.0
mysqlclient==2.0.1
Pillow==7.2.0
```

## Configurar app/settings.py
```python
import os
from django.contrib.messages import constants as message_constants
from .database import MYSQL

# ...


# Application definition

INSTALLED_APPS = [
    # ...

    # PACKAGES
    'crispy_forms',

    # APPS
]


# ...


TEMPLATES = [
    {
        # ...
        'DIRS': [BASE_DIR / 'templates'], # CONFIGURE TEMPLATES DIR
        # ...
    },
]

# ...

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = MYSQL


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# ...


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# ...

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '5a2ab0e62e69be'
EMAIL_HOST_PASSWORD = '1a4b741007de81'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# template formularios bootstrap 4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# clases para los mensajes flash de bootstrap
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger'
}

# urls para archivos media de base de datos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Create products app

### Update productos/models.py
```python
from django.db import models


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=300)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['id']


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productos/', blank=True)
    excerpt = models.TextField(max_length=200, verbose_name='Extracto')
    detail = models.TextField(max_length=1000, verbose_name='Información del producto')
    price = models.FloatField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
```

### Update productos/admin.py
```python
from django.contrib import admin

from .models import Category, Product

admin.site.register([Category, Product])
```

### Update productos/views.py for show products
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from productos.models import Product


@login_required(login_url='/autenticacion/acceder')
def listado_productos(request):
    productos = Product.objects.all()
    return render(request, 'productos/listado.html', {
        "productos": productos
    })
```

### Update productos/urls.py
```python
from django.urls import path
from .views import listado_productos

urlpatterns = [
    path('', listado_productos, name='listado_productos')
]
```

### Update app/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacion/', include('autenticacion.urls')),
    path('productos/', include('productos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Create layout base templates/layouts/tienda.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %} - Cursosdesarrolloweb</title>

    {% load static %}
    <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet"/>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">Tienda Python y Django</a>
        <button
            class="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'listado_productos' %}">Tienda</a>
                </li>
            </ul>

            <ul class="navbar-nav ml-auto">
                {% if user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="#">Mis pedidos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Hola {{ user.username }}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'salir' %}">Cerrar sesión</a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'acceder' %}">Acceder</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'registro' %}">Registro</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </nav>

    <div class="container mt-3">
        {% if messages %}
            <div class="row mt-3 mb-3">
                <div class="col-12">
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            </div>
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <script src="{% static 'js/jquery-slim.min.js' %}"></script>
    <script src="{% static 'js/popper.min.js' %}"></script>
    <script src="{% static 'js/bootstrap.min.js' %}"></script>
</body>

</html>
```

### Update templates/productos/listado.html
```html
{% extends 'layouts/tienda.html' %}

{% block title %}Blog{% endblock %}

{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-9">
                <div class="row">
                    {% for product in productos %}
                        <div class="col-md-3 col-sm-12 col-lg-4">
                            <div class="card" style='width:100%'>
                                <img src="{{ product.image.url }}" style="width:100%;" class="card-img-top" alt="{{ product.name }}">
                                <div class="card-body">
                                    <h5 class="card-title"> {{ product.name }}</h5>
                                    <p class="card-text">{{ product.extracto }}</p>
                                </div>
                                <div class='card-footer text-center'>
                                    <a href="#" class="btn btn-success">Añadir al carrito</a>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
            <div class="col-3">
                {% comment %}Aquí va el widget del carrito{% endcomment %}
            </div>
        </div>
    </div>
{% endblock %}
```

### Register app on settings.py
```python
INSTALLED_APPS = [
    # APPS
    'productos',

]
```

## Create carrito app
### Create cart class carrito/cart.py
```python
# django-shopping-cart
class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                'product_id': product.id,
                'name': product.name,
                'quantity': 1,
                'price': str(product.price),
                'image': product.image.url
            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value['quantity'] = value['quantity'] + 1
                    self.save()
                    break

        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantity'] = value['quantity'] - 1
                if value['quantity'] < 1:
                    self.remove(product)
                self.save()
                break
            else:
                print("El producto no existe en el carrito")

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
```

### Update carrito/views.py
```python
from django.shortcuts import redirect
from productos.models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart


@login_required(login_url="/autenticacion/login")
def add_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect("listado_productos")


@login_required(login_url="/autenticacion/login")
def remove_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect("listado_productos")


@login_required(login_url="/autenticacion/login")
def decrement_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.decrement(product=product)
    return redirect("listado_productos")


@login_required(login_url="/autenticacion/login")
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("listado_productos")
```

### Create carrito/templatetags files
```python
from django import template

register = template.Library()


# return value * quantity
@register.filter()
def multiply(value, arg):
    return float(value) * arg


# return 400.0€
@register.filter()
def money_format(value, arg):
    return f"{value}{arg}"
```

### Create cart context processor for calculate total cart
```python
def cart_total_amount(request):
	total = 0.0
	if request.user.is_authenticated:
		for key, value in request.session['cart'].items():
			total = total + (float(value['price']) * value['quantity'])
	return {'cart_total_amount': total}
```

### Register context processor on settings.py
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'carrito.context_processor.cart_total_amount',
            ],
        },
    },
]
```

### Create templates/carrito/widget.html
```html
{% load carrito_tags %}
<table class="table table-bordered">
    <thead>
        <tr>
            <th colspan="3" class="text-center">
                Carrito de compras
            </th>
        </tr>
        <tr>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {% if request.session.cart.items %}
           {% for key, value in request.session.cart.items %}
                <tr class="text-center">
                    <td>{{ value.name }}</td>
                    <td>{{ value.quantity }}</td>
                    <td>
                        <a href="{% url 'cart:add_product' value.product_id %}" class="btn btn-sm btn-success">+</a>
                        <a href="{% url 'cart:decrement_product' value.product_id %}" class="ml-2 btn-sm btn btn-danger">-</a>
                        Total {{ value.price|multiply:value.quantity|money_format:"€" }}
                    </td>
                </tr>
            {% endfor %}
        {% else %}
            <tr>
                <td colspan="3">
                    <div class="alert alert-danger text-center">No tienes productos en el carrito</div>
                </td>
            </tr>
        {% endif %}
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3">
                Total: {{ cart_total_amount|money_format:"€" }}
            </td>
        </tr>
        {% if request.session.cart.items %}
            <tr>
                <td colspan="3">
                    <a href="{% url 'crear_pedido' %}" class="btn btn-success">Crear pedido</a>
                </td>
            </tr>
        {% endif %}
    </tfoot>
</table>
```

### Update carrito/urls.py
```python
from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path('add_product/<int:product_id>/', add_product, name='add_product'),
    path('remove_product/<int:product_id>/', remove_product, name='remove_product'),
    path('decrement_product/<int:product_id>/', decrement_product, name='decrement_product'),
    path('clear/', clear_cart, name='clear_cart'),
]
```

### Update app/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacion/', include('autenticacion.urls')),
    path('productos/', include('productos.urls')),
    path('carrito/', include('carrito.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Create and register pedidos app
### Update pedidos/models.py
```python
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F, Sum, FloatField

from productos.models import Product

# Get the user model
User = get_user_model()


# Order Model
class Order(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ordenado = models.BooleanField(default=False)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.orderline_set.aggregate(
            total=Sum(F('producto__price') * F('cantidad'), output_field=FloatField())
        )["total"] or FloatField(0)

    def __str__(self):
        return self.usuario.username

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']


# OrderLine Model
class OrderLine(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Order, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} of {self.producto.name}'

    class Meta:
        db_table = 'lineas_pedidos'
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedidos'
        ordering = ['id']
```

### Register models on admin
```python
from django.contrib import admin
from pedidos.models import Order, OrderLine

admin.site.register([Order, OrderLine])
```

### Update pedidos views
```python
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import DetailView
from pedidos.models import OrderLine, Order
from django.contrib import messages
from carrito.cart import Cart
from django.views.generic.list import ListView


@login_required(login_url='/autenticacion/acceder')
def crear_pedido(request):
    pedido = Order.objects.create(usuario=request.user, ordenado=True)
    carrito = Cart(request)
    lineas_pedido = list()
    for key, value in carrito.cart.items():
        lineas_pedido.append(
            OrderLine(producto_id=value['product_id'], cantidad=value['quantity'], usuario=request.user, pedido=pedido)
        )

    OrderLine.objects.bulk_create(lineas_pedido)

    carrito.clear()

    enviar_correo(
        pedido=pedido, lineas_pedido=lineas_pedido, user_email=request.user.email, username=request.user.username
    )

    messages.success(request, f"¡El pedido ha sido creado!")
    return redirect("listado_productos")


class ListadoPedidos(ListView):
    model = Order
    ordering = ["-id"]
    template_name = 'pedidos/listado.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)


class DetallePedido(DetailView):
    model = Order
    template_name = 'pedidos/detalle.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)


def enviar_correo(**kwargs):
    subject = 'Gracias por tu pedido'
    html_message = render_to_string('emails/nuevo_pedido.html', {
        'pedido': kwargs.get("pedido"),
        'lineas_pedido': kwargs.get("lineas_pedido"),
        'username': kwargs.get("username")
    })
    plain_message = strip_tags(html_message)
    from_email = 'admin@yourdjangoapp.com'
    to = kwargs.get("user_email")
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
```

### Udpate urls pedidos
```python
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('crear_pedido', crear_pedido, name='crear_pedido'),
    path('mios', login_required(ListadoPedidos.as_view(), login_url='/autenticacion/acceder'), name='mis_pedidos'),
    path('<int:pk>', login_required(DetallePedido.as_view(), login_url='/autenticacion/acceder'), name='detalle_pedido'),
]
```

### Create templates/pedidos/listado.html
```html
{% extends 'layouts/tienda.html' %}

{% load carrito_tags %}

{% block title %}Mis pedidos{% endblock %}

{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-9">
                <div class="row">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Total</th>
                                <th>Fecha</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for order in object_list %}
                                <tr>
                                    <td>{{ order.id }}</td>
                                    <td>{{ order.total|money_format:"€" }}</td>
                                    <td>{{ order.fecha_alta|date:'d/m/Y H:i' }}</td>
                                    <td><a href="{% url 'detalle_pedido' order.id %}" class="btn btn-info btn-sm">Ver detalle</a></td>
                                </tr>
                            {% empty %}
                                <tr>
                                    <td colspan="4">
                                        <div class="alert alert-danger">No tienes ningún pedido todavía.</div>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

### Create templates/pedidos/detalle.html
```html
{% extends 'layouts/tienda.html' %}

{% load carrito_tags %}

{% block title %}Detalle del pedido #{{ order.id }}#{% endblock %}

{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center text-muted">Detalle del pedido #{{ order.id }}#</h1>
                <table class="table table-bordered">
                    <thead>
                        <tr class="text-center">
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Precio/u</th>
                            <th>Precio total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for order_line in order.orderline_set.all %}
                           <tr class="text-center">
                                <td>{{ order_line.producto.name }}</td>
                                <td>{{ order_line.cantidad }}</td>
                                <td>{{ order_line.producto.price|money_format:"€" }}</td>
                                <td>{{ order_line.producto.price|multiply:order_line.cantidad|money_format:"€" }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td>&nbsp;</td>
                            <td>&nbsp;</td>
                            <td>&nbsp;</td>
                            <td class="text-center">
                                {{ order.total|money_format:"€" }}
                            </td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
{% endblock %}
```