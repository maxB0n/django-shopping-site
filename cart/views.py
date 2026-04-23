from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import Product

def cart_summary(request):
    cart = Cart(request)
    cart_items = []
    
    # Bundle the product and its quantity together into a list
    for product_id, item_data in cart.cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'total_item_price': product.price * item_data['quantity']
        })
        
    # Send that bundled list to the HTML
    return render(request, 'cart/cart_summary.html', {'cart_items': cart_items})

def cart_add(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # Grab the quantity from the HTML form (make sure it's a number)
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)
        
        # Send the quantity to our cart logic
        cart.add(product=product, quantity=quantity)
        
        #This tells Django to send the user right back to the page they were just on
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
def cart_delete(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        # Grab the product ID from the hidden input in the form
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Run our new delete function
        cart.delete(product=product)
        
        # Reload the cart page
        return redirect('cart_summary')