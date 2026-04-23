from django.db import models
from products.models import Product

class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    shipping_address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"


class OrderItem(models.Model):
    # This tether links the item to a specific Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # This tether links the item to a specific Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # We save the price here to lock it in permanently, even if the product price changes next year!
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"