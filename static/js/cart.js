$(document).ready(function () {
    $('.add-to-cart-btn').on('click', function (event) {
      event.preventDefault() // Prevent default behavior (like form submission)

      const productId = $(this).data('product-id') // Get the product ID from the button

      $.ajax({
        url: "{% url 'cart-add' %}", // The URL for the cart-add view
        type: 'POST', // Ensure we're using POST for adding to the cart
        data: {
          product_id: productId, // Product ID to be added to the cart
          csrfmiddlewaretoken: '{{ csrf_token }}' // CSRF token for security
        },
        success: function (response) {
          if (response.success) {
            // Expecting 'success' as a response from the server
            // Update the cart quantity and total price in the UI
            $('#cart-quantity').text(response.cart_item_quantity) // Updated item quantity
            $('#cart-total-price').text(response.cart_total_price) // Updated total price

            // Optionally, show a success message or update the cart icon with a badge
            // Example: $('#cart-icon').addClass('cart-updated');
          } else {
            // Handle failure (e.g., show an error message)
            alert('Error adding item to cart')
          }
        },
        error: function (xhr, status, error) {
          console.error('Error:', error)
          alert('There was an error with your request.')
        }
      })
    })
  })