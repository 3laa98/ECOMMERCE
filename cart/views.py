from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from store.models import Product

from .models import Cart, CartItem


def get_cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user, is_active=True if request.user.is_authenticated else None
    )
    return cart


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Cart, CartItem, Product


@login_required
@require_POST
def cart_add(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        quantity = int(request.POST.get('quantity', 1))
        print(quantity)

        if not product_id:
            return JsonResponse(
                {'success': False, 'error': 'Product ID is required'}, status=400
            )

        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        cart_items = cart.items.all()

        # Calculate total quantity and price
        cart_total_quantity = sum(item.quantity for item in cart_items)
        cart_total_price = sum(
            item.product.price * item.quantity for item in cart_items
        )

        # Render updated cart items HTML
        cart_items_html = render_to_string(
            'cart/partial/cart_list.html',
            {'cart_items': cart_items, 'csrf_token': csrf_token},
        )

        return JsonResponse(
            {
                'success': True,
                'cart_item_quantity': cart_item.quantity,
                'cart_total_quantity': cart_total_quantity,
                'cart_total_price': cart_total_price,
                'cart_items_html': cart_items_html,  # Return the HTML of cart items
            }
        )

    return JsonResponse(
        {'success': False, 'error': 'Invalid request', 'message': 'Invalid request'},
        status=400,
    )


@login_required
@require_POST
def cart_remove(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        item_id = request.POST.get('item_id')
        csrf_token = request.POST.get('csrfmiddlewaretoken')

        if not item_id:
            return JsonResponse(
                {'success': False, 'error': 'Item ID is required'}, status=400
            )

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = get_cart(request)
        try:
            CartItem.objects.filter(cart=cart, id=item_id).delete()
            cart_items = cart.items.all()

            # Calculate total quantity and price
            cart_total_quantity = sum(item.quantity for item in cart_items)
            cart_total_price = sum(
                item.product.price * item.quantity for item in cart_items
            )

            # Render updated cart items HTML
            cart_items_html = render_to_string(
                'cart/partial/cart_list.html',
                {'cart_items': cart_items, 'csrf_token': csrf_token},
            )

            return JsonResponse(
                {
                    'success': True,
                    'cart_item_quantity': cart_item.quantity,
                    'cart_total_quantity': cart_total_quantity,
                    'cart_total_price': cart_total_price,
                    'cart_items_html': cart_items_html,  # Return the HTML of cart items
                    'message': 'Item removed from cart.',
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Item not found in cart.'}, status=404
            )


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
