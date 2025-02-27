from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from store.models import Product
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string

from .models import Cart, CartItem


def get_cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None
    )
    return cart


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required


@login_required
@require_POST
def cart_add(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')

        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)  # Assuming you have this method to retrieve the user's cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_items = cart.items.all()

        # Calculate total quantity and price
        cart_total_quantity = sum(item.quantity for item in cart_items)
        cart_total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Render updated cart items HTML
        cart_items_html = render_to_string('cart/partial/cart_list.html', {'cart_items': cart_items})

        return JsonResponse({
            'success': True,
            'cart_item_quantity': cart_item.quantity,
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'cart_items_html': cart_items_html,  # Return the HTML of cart items
        })

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)



@login_required
def cart_remove(request, product_id):
    cart = get_cart(request)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return redirect('cart-detail')


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
