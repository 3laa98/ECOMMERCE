// static/js/cart.js
function addToCart(productId, quantity, csrfToken, cartAddUrl) {
  $.ajax({
    url: cartAddUrl, // URL to your cart-add view
    type: 'POST',
    data: {
      product_id: productId, // Send the product ID
      csrfmiddlewaretoken: csrfToken, // CSRF token for security
      quantity: quantity
    },
    success: function (response) {
      if (response.success) {
        // Update the cart quantity and price in the UI
        $('#cart_qty').text(response.cart_total_quantity);
        $('.cart-summary h5').text('SUBTOTAL: $' + response.cart_total_price);
        $('.cart-summary small').text(response.cart_total_quantity + ' Item(s) selected');
        // Update the cart items container with the new HTML
        $('.cart-list').html(response.cart_items_html);
        // Optionally show a success notification
        Swal.fire({
          icon: 'success',
          title: 'Item added to cart',
          text: 'Your item has been added to the cart.',
          timer: 2000,
          showConfirmButton: false
        });
      } else {

        // Handle failure to add item to cart
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Failed to add item to cart.'
        });
      }
    },
    error: function (xhr, status, error) {
      // Handle AJAX error
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'Something went wrong. Please try again.'
      });
    }
  });
}

function deleteFromCart(itemId, csrfToken, cartDeleteUrl) {
  $.ajax({
    url: cartDeleteUrl, // URL to your cart-add view
    type: 'POST',
    data: {
      item_id: itemId, // Send the product ID
      csrfmiddlewaretoken: csrfToken // CSRF token for security
    },
    success: function (response) {
      if (response.success) {
        // Update the cart quantity and price in the UI
        $('#cart_qty').text(response.cart_total_quantity);
        $('.cart-summary h5').text('SUBTOTAL: $' + response.cart_total_price);
        $('.cart-summary small').text(response.cart_total_quantity + ' Item(s) selected');
        // Update the cart items container with the new HTML
        $('.cart-list').html(response.cart_items_html);

        // Optionally show a success notification
        Swal.fire({
          icon: 'success',
          title: 'Item deleted from cart',
          text: 'Your item has been deleted from the cart.',
          timer: 2000,
          showConfirmButton: false
        });
      } else {
        console.log(response.message)
        // Handle failure to add item to cart
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Failed to Delete item to cart.'
        });
      }
    },
    error: function (xhr, status, error) {
      // Handle AJAX error
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'Something went wrong. Please try again.'
      });
    }
  });
}

$(document).ready(function () {
  $('.add-to-cart-btn').on('click', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const productId = $(this).data('product-id'); // Get the product ID from the button
    const csrfToken = $(this).data('csrf-token'); // Get the CSRF token from the button
    const cartAddUrl = $(this).data('cart-add-url'); // Get the cart-add URL from the button
    const quantity = $(this).attr('data-quantity');

    // Call the global function
    addToCart(productId, quantity, csrfToken, cartAddUrl);
  });
});


$(document).ready(function () {
  // Use event delegation for dynamically added .delete buttons
  $('.cart-list').on('click', '.delete', function (event) {
    event.preventDefault();
    console.log('Delete button clicked');// Prevent the default form submission

    const ItemId = $(this).data('cart-item-id'); // Get the product ID from the button
    const csrfToken = $(this).data('csrf-token'); // Get the CSRF token from the button
    const cartDeleteUrl = $(this).data('cart-delete-url'); // Get the cart-add URL from the button

    // Call the global function
    deleteFromCart(ItemId, csrfToken, cartDeleteUrl);
  });
});
