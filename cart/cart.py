from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
    def update(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] = int(product_qty)
            self.session.modified = True
            
    def delete(self, product):
        product_id = str(product)
        if product_id and self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    unit_price = product.price
                    if product.is_sale:
                        unit_price = product.sale_price
                    
                    total = total + (unit_price * value)
        return total
            
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
        
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def get_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []

        for product in products:
            quantity = self.cart[str(product.id)]
            price = product.sale_price if product.is_sale else product.price
            items.append({
                'product': product,
                'quantity': quantity,
                'price': price * quantity
            })
        return items
    
    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True