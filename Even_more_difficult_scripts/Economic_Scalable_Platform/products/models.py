# products/models.py

# Import the necessary modules
from django.db import models
from accounts.models import User

# Define the Product model
class Product(models.Model):
    name = models.CharField(max_length=200)  # The name of the product, a string of max length 200
    description = models.TextField()  # The description of the product, a text field without a specified limit
    price = models.DecimalField(max_digits=5, decimal_places=2)  # The price of the product, a decimal with 5 digits in total and 2 decimal places
    stock = models.IntegerField()  # The stock level of the product, an integer

# Define the Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who placed the order, a foreign key referencing the User model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product ordered, a foreign key referencing the Product model
    quantity = models.IntegerField()  # The quantity of the product ordered, an integer
    total_price = models.DecimalField(max_digits=5, decimal_places=2)  # The total price of the order, a decimal with 5 digits in total and 2 decimal places
    created_at = models.DateTimeField(auto_now_add=True)  # The date and time when the order was placed, automatically set to the current date and time when the order is created

# Define the Cart model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # The user who owns the cart, a one-to-one field referencing the User model

# Define the CartItem model
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product in the cart, a foreign key referencing the Product model
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # The cart that contains the item, a foreign key referencing the Cart model
    quantity = models.IntegerField()  # The quantity of the product in the cart, an integer