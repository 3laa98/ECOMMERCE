import json

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from order.models import Order

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    return render(
        request,
        'order/checkout.html',
        {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY},
    )


def create_order(user, cart):
    order = Order.objects.create(
        user=user, cart=cart, total_price=cart.get_cart_total()
    )
    cart.is_active = False
    cart.save()

    return order


def get_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/orders.html', context={'orders': orders})
