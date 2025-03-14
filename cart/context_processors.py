from cart.models import Cart


def get_cart(request):
    """Get or create a cart for the authenticated user."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    else:
        # You can return None or a cart for guests (optional behavior)
        cart = None
    return cart


def get_cartitems(request):
    """Retrieve cart items, total, and count for the user."""
    cart = get_cart(request)

    # Initialize cart-related variables
    if cart:
        cart_items = cart.items.all()  # Get all items in the cart
        cart_total_price = (
            cart.get_cart_total()
        )  # Use model method to calculate total price
        cart_total_quantity = (
            cart.get_cart_count()
        )  # Use model method to count total items
    else:
        cart_items = []
        cart_total_quantity = 0
        cart_total_price = 0

    return {
        "cart_items": cart_items,
        "cart_total_quantity": cart_total_quantity,
        "cart_total_price": cart_total_price,
    }
