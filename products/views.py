from django.shortcuts import render
from .models import Product

def product_list(request):
    # Grab all the products from the database
    products = Product.objects.all()
    # Send them to an HTML file called 'product_list.html'
    return render(request, 'products/product_list.html', {'products': products})