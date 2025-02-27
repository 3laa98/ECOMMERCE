from django.contrib.auth.models import User
from django.db import models

from store.models import Product

# Create your models here.


class Cart(models.Model):
    """Model definition for Cart."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Cart."""

        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        """Unicode representation of Cart."""
        return f"Cart ({self.user.username})"

    def get_cart_total(self):
        """Method to calculate total price of items in the cart."""
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total

    def get_cart_count(self):
        """Method to count total number of items in the cart."""
        count = sum(item.quantity for item in self.items.all())
        return count


class CartItem(models.Model):
    """Model definition for CartItem."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        """Meta definition for CartItem."""

        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        """Unicode representation of CartItem."""
        return f"{self.product.name} (x{self.quantity}) in Cart {self.cart.id}"
