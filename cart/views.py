from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.cart_total()
    for product in cart_products:
        product.quantity = quantities.get(str(product.id), 1)
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'total': total})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        # Get current cart quantity for this product
        product_data = cart.cart.get(str(product_id), {})
        current_cart_qty = product_data.get('quantity', 0) if isinstance(product_data, dict) else 0


        total_requested_qty = current_cart_qty + product_qty

        if total_requested_qty <= product.stock_quantity:
            cart.add(product=product, quantity=product_qty)
            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity})
            messages.success(request, "Item Added to Cart successfully .. ")
            return response
        else:
            messages.error(request, f"Only {product.stock_quantity - current_cart_qty} items available in stock.")
            return JsonResponse({'error': f"Only {product.stock_quantity - current_cart_qty} items available in stock."}, status=400)

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item Deleted from Cart successfully .. "))
        return response
    

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Item Quantity Updated successfully .. "))
        return response