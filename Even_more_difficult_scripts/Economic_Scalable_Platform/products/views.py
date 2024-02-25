# products/views.py

# Import necessary modules and models
from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem

# Define a view to display the current user's shopping cart
def view_cart(request):
    # Get the cart for the current user
    cart = Cart.objects.get(user=request.user)
    # Render the 'cart.html' template, passing the user's cart as context
    return render(request, 'cart.html', {'cart': cart})

# Define a view to add a product to the current user's shopping cart
def add_to_cart(request, product_id):
    # Get the product with the given id
    product = Product.objects.get(id=product_id)
    # Get the cart for the current user, or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Create a new cart item for the product, adding it to the user's cart
    CartItem.objects.create(product=product, cart=cart, quantity=1)
    # Redirect to the 'view_cart' view
    return redirect('view_cart')

# Define a view to remove an item from the current user's shopping cart
def remove_from_cart(request, item_id):
    # Get the cart item with the given id
    item = CartItem.objects.get(id=item_id)
    # If the current user is the owner of the cart that contains the item, delete the item
    if request.user == item.cart.user:
        item.delete()
    # Redirect to the 'view_cart' view
    return redirect('view_cart')