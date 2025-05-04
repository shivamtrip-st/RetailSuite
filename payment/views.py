from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from payment.forms import ShippingForm
from payment.models import Order, OrderItem, ShippingAddress
from store.models import Product
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import stripe
from django.conf import settings
from django.http import JsonResponse

@login_required
def create_checkout_session(request):
    cart = Cart(request)
    shipping_address, _ = ShippingAddress.objects.get_or_create(user=request.user)

    line_items = []
    for item in cart.get_items():
        product = item['product']
        quantity = item['quantity']
        price = int(product.sale_price if product.is_sale else product.price)
        
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(price * 100),
            },
            'quantity': quantity,
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/payment/success').rstrip('/') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri('/payment/cancel/'),
        metadata={
            'user_id': request.user.id,
            'shipping_id': shipping_address.id
        }
    )
    return JsonResponse({'id': session.id})

        
@login_required
def checkout_shipping(request):
    shipping_address, _ = ShippingAddress.objects.get_or_create(user=request.user)
    form = ShippingForm(request.POST or None, instance=shipping_address)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('checkout_review')

    return render(request, 'payment/checkout_shipping.html', {'form': form})

@login_required
def checkout_review(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    shipping_address, _ = ShippingAddress.objects.get_or_create(user=request.user)
    form = ShippingForm(instance=shipping_address)

    return render(request, 'payment/checkout_review.html', {
        'cart_items': cart_items,
        'shipping_address': shipping_address,
        'form': form,
        'total': cart.cart_total(),
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
def checkout_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('checkout_review')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    user_id = session.metadata.get('user_id')
    shipping_id = session.metadata.get('shipping_id')

    if not user_id or int(user_id) != request.user.id:
        return redirect('checkout_review')

    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()

    shipping_address = ShippingAddress.objects.get(id=shipping_id)

    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        total_paid=session.amount_total / 100,
        is_paid=True,
    )

    for product in cart_products:
        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.sale_price if product.is_sale else product.price,
            quantity=quantities.get(str(product.id), 1)
        )
        ordered_qty = quantities.get(str(product.id), 1)
        product.sell(ordered_qty)

    cart.clear()
    if 'cart' in request.session:
        del request.session['cart']

    request.user.profile.old_cart = json.dumps({})
    request.user.profile.save()

    messages.success(request, "Order placed successfully after payment!")
    return render(request, 'payment/payment_success.html', {'session':session, 'order':order})


@login_required
def checkout_complete(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    shipping_address, _ = ShippingAddress.objects.get_or_create(user=request.user)
    form = ShippingForm(request.POST, instance=shipping_address)


    if request.method == "POST" and form.is_valid():
        shipping = form.save()
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping,
            total_paid=cart.cart_total(),
            is_paid=False
        )

        for product in cart_products:
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.sale_price if product.is_sale else product.price,
                quantity=quantities.get(str(product.id), 1)
            )
            ordered_qty = quantities.get(str(product.id), 1)
            product.sell(ordered_qty)

        cart.clear()
        if 'cart' in request.session:
            del request.session['cart']

        request.user.profile.old_cart = json.dumps({})
        request.user.profile.save()

        messages.success(request, "Order placed successfully!")
        return redirect('payment_success')

    return render(request, 'payment/checkout_review.html', {
        'form': form,
        'cart_products': cart_products,
        'total': cart.cart_total()
    })


# Create your views here.

def payment_success(request):
	return render(request, "payment/payment_success.html", {})

def checkout_cancel(request):
	return render(request, "payment/payment_failed.html", {})

@login_required
def order_history(request):
    filter_param = request.GET.get('filter')
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    if filter_param == 'shipped':
        orders = orders.filter(is_shipped=True)
    elif filter_param == 'unshipped':
        orders = orders.filter(is_shipped=False)

    return render(request, 'payment/order_history.html', {
        'orders': orders,
        'is_admin': request.user.is_staff,
        'filter_param': filter_param,
    })

@login_required
def toggle_shipped_status(request, order_id):
    if not request.user.is_staff:
        return redirect('order_history')
    order = get_object_or_404(Order, id=order_id)
    order.is_shipped = not order.is_shipped
    order.save()
    messages.success(request, "Order status updated successfully!")
    return redirect('order_history')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    shipping_address = ShippingAddress.objects.filter(order=order).first()
    if not request.user.is_staff and order.user != request.user:
        return redirect('order_history')

    return render(request, 'payment/order_detail.html', {
        'order': order,
        'shipping_address': shipping_address,
    })
