from django.shortcuts import render
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from cart.models import Cart
from order.views import create_order
# Create your views here.

@csrf_exempt
def create_payment_intent(request):
    if request.method == "POST":
        try:
            # Get cart total from frontend
            data = json.loads(request.body)
            cart = Cart.objects.get(user=request.user, is_active=True)
            total_amount = int(cart.get_cart_total() * 100)  # Convert to cents

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency="usd",
                payment_method_types=["card"]
            )

            order = create_order(request.user, cart)

            return JsonResponse({"clientSecret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def success(request):
    """Render success page after payment."""
    return render(request, "order/success.html")

def cancel(request):
    """Render cancel page if payment is canceled."""
    return render(request, "order/cancel.html")