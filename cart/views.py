from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product

from .models import Cart, CartItem


def get_cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None
    )
    return cart


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


@login_required
def cart_remove(request, product_id):
    cart = get_cart(request)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    return render(request, 'cart/cart_details.html', {})
    cart = get_cart(request)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.total_price() for item in cart_items)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX check
        return JsonResponse(
            {
                'status': 'success',
                'quantity': cart_items.quantity,
                'total_price': cart_items.total_price(),
            }
        )
    return render(
        request,
        'cart/detail.html',
        {'cart_items': cart_items, 'total_price': total_price},
    )
