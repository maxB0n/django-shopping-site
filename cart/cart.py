from decimal import Decimal
from products.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # Get the current session key if the user already has one
        cart = self.session.get('session_key')
        
        # If they are a brand new user, build them an empty cart dictionary
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
    def __iter__(self):
        # Get the product IDs that are in the cart
        product_ids = self.cart.keys()
        # Fetch those products from the database
        products = Product.objects.filter(id__in=product_ids)
        
        # Copy the cart to add the actual product objects to it
        import copy
        cart = copy.deepcopy(self.cart)
        
        for product in products:
            # Add the product object to the cart data
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # Convert price to Decimal and calculate total for the template
            item['price'] = Decimal(item['price'])
            item['total_item_price'] = item['price'] * item['quantity']
            yield item
            
    def add(self, product, quantity=1):
        product_id = str(product.id)
        
        # If it's already in the cart, just add to the existing quantity
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            # If it's new, save the price AND the starting quantity
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}
            
        self.session.modified = True
    def get_products(self):
        # Get all the product IDs currently in the cart
        product_ids = self.cart.keys()
        # Look up those specific IDs in the database
        products = Product.objects.filter(id__in=product_ids)
        return products
    def get_total_price(self):
        total = 0
        # Multiply the price by the quantity for every item
        for item in self.cart.values():
            total += float(item['price']) * item['quantity']
        return total
    def delete(self, product):
        product_id = str(product.id)
        
        # If the item exists in the cart, delete it
        if product_id in self.cart:
            del self.cart[product_id]
            # Tell Django we changed the session
            self.session.modified = True
