from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.list import ListView
from django.views.generic import DetailView

from autenticacion.views import GuestOrderForm, render
from products.models import Product

"correos"
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import Order, OrderLine

from cart.cart import Cart


"""
# Create your views here.
#@login_required(login_url='/autenticacion/acceder')
def process_order(request):
    user = request.user if request.user.is_authenticated else None
    order = Order.objects.create(user=request.user, completed=True)
    cart = Cart(request)
    order_lines = list()
    for key, value in cart.cart.items():
        order_lines.append(
            OrderLine(
                product_id=key,
                quantity=value["quantity"],
                user=request.user,
                order=order
            )
        )

    OrderLine.objects.bulk_create(order_lines)
    
    send_order_email(
        order=order,
        order_lines=order_lines,
        username=request.user.username,
        user_email=request.user.email
    )

    cart.clear()

    messages.success(request, "El pedido se ha creado correctamente!")
    return redirect("listado_productos")


def send_order_email(**kwargs):
    subject = "Gracias por tu pedido"
    html_message = render_to_string("emails/nuevo_pedido.html", {
        "order": kwargs.get("order"),
        "order_lines": kwargs.get("order_lines"),
        "username": kwargs.get("username")
    })
    plain_message = strip_tags(html_message)
    from_email = "karlosmya14@gmail.com"
    to = kwargs.get("user_email")
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


class OrderList(ListView):
    model = Order
    ordering = ["-id"]
    template_name = "orders/listado.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OrderDetail(DetailView):
    model = Order
    template_name = "orders/detalle.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
"""


def process_order(request):
    if request.user.is_authenticated:
        return _create_order(request, user=request.user)
    else:
        if request.method == 'POST':
            form = GuestOrderForm(request.POST)
            if form.is_valid():
                return _create_order(
                    request,
                    user=None,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email']
                )
        else:
            form = GuestOrderForm()
        return render(request, 'autenticacion/formularioInvitado.html', {'form': form})






def _create_order(request, user, first_name=None, last_name=None, email=None):
    order = Order.objects.create(user=user, completed=True)
    cart = Cart(request)
    order_lines = list()
    total = 0
    for key, value in cart.cart.items():
        product = Product.objects.get(id=key)
        quantity = value["quantity"]
        order_lines.append(
            OrderLine(
                product=product,
                quantity=quantity,
                user=user,
                order=order
            )
        )
        total += product.price * quantity

        request.session['total'] = total


    OrderLine.objects.bulk_create(order_lines)

    if user:
        send_order_email(
            order=order,
            order_lines=order_lines,
            username=user.username,
            user_email=user.email
        )
    else:
        send_order_email(
            order=order,
            order_lines=order_lines,
            username=f"{first_name} {last_name}",
            user_email=email
        )

    cart.clear()

    messages.success(request, "El pedido se ha creado correctamente!")
    #return redirect("listado_productos")
    #retornamos una web para los usuarios no registrados
    return render(request, "orders/pedidoCorrecto.html",{'order': order, 'order_lines': order_lines, 'total': total})



"""Correos API
def send_order_email(**kwargs):
    subject = "Gracias por tu pedido"
    html_message = render_to_string("emails/nuevo_pedido.html", {
        "order": kwargs.get("order"),
        "order_lines": kwargs.get("order_lines"),
        "username": kwargs.get("username")
    })
    plain_message = strip_tags(html_message)
    from_email = "karlosmya14@gmail.com"
    to = kwargs.get("user_email")
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

"""


def send_order_email(**kwargs):
    subject = "Gracias por tu pedido"

    # Renderizar el mensaje HTML usando una plantilla de Django
    html_message = render_to_string("emails/nuevo_pedido.html", {
        "order": kwargs.get("order"),
        "order_lines": kwargs.get("order_lines"),
        "username": kwargs.get("username")
    })
    plain_message = strip_tags(html_message)
    from_email = "karlosmya14@gmail.com"
    to_email = kwargs.get("user_email")

    # Crear el mensaje MIMEMultipart
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    # Adjuntar las versiones de texto plano y HTML al mensaje
    part1 = MIMEText(plain_message, "plain")
    part2 = MIMEText(html_message, "html")
    msg.attach(part1)
    msg.attach(part2)

    # Configurar el servidor SMTP y enviar el correo
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, "Ca18091998.")
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


class OrderList(ListView):
    model = Order
    ordering = ["-id"]
    template_name = "orders/listado.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OrderDetail(DetailView):
    model = Order
    template_name = "orders/detalle.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)



