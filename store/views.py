import json
from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Review, Order
from cart.cart import Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from payment.models import ShippingAddress, Product
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ReviewForm
from payment.forms import ShippingForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    categories = Category.objects.all()
    category_name = request.GET.get('category')
    selected_category = None
    query_filters = Q()
    if category_name:
        try:
            category_obj = Category.objects.get(name=category_name)
            query_filters &= Q(category=category_obj)
            selected_category = category_name
        except Category.DoesNotExist:
            messages.warning(request, f"Category '{category_name}' does not exist.")

    query = request.GET.get('query')
    if query:
        search_filters = Q(name__icontains=query) | Q(description__icontains=query)
        query_filters &= search_filters
        messages.info(request, f'Search results for "{query}"')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            min_price = float(min_price)
            query_filters &= Q(price__gte=min_price)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            query_filters &= Q(price__lte=max_price)
        except ValueError:
            pass

    if query_filters:
        products = Product.objects.filter(query_filters)
    else:
        products = Product.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
    }
    
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                profile = user.profile
                if profile.old_cart:
                    request.session['cart'] = json.loads(profile.old_cart)
            except:
                pass
            messages.success(request, ("You Have Been Logged In Succesfully"))
            return redirect('home')
        else:
            messages.success(request, ("There was error in logging in pleaase try again .."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    if request.user.is_authenticated:
        cart_data = request.session.get('cart', {})
        if cart_data:
            Profile.objects.update_or_create(
                user=request.user,
                defaults={'old_cart': json.dumps(cart_data)}
            )
    logout(request)
    messages.success(request, ('Your have been logged out successfully'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have Been Registered Succesfully, Please fill out the personal details below"))
            return redirect('update_info')
        else:
            messages.success(request, ("There was error in registering you in please try again .."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Use Has Been Updated !!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in for Updating profile !!")
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Profile Information Has Been Updated !!")
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You must be logged in for Updating profile !!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Passworde changed successfully"))
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to change your password")
        return redirect('home')
    
def inventory_report(request):
    products = Product.objects.all()

    if request.method == 'POST':
        for product in products:
            restock_key = f"restock_{product.id}"
            sell_key = f"sell_{product.id}"
            if restock_key in request.POST:
                restock_quantity = request.POST.get(restock_key)
                try:
                    restock_quantity = int(restock_quantity)
                    if restock_quantity >= 0:
                        product.restock(restock_quantity)
                    else:
                        messages.error(request, f"Invalid restock quantity for {product.name}. It must be a positive number.")
                except ValueError:
                    messages.error(request, f"Invalid restock quantity for {product.name}. Please enter a valid number.")
            if sell_key in request.POST:
                sell_quantity = request.POST.get(sell_key)
                try:
                    sell_quantity = int(sell_quantity)
                    if sell_quantity >= 0:
                        product.sell(sell_quantity)
                    else:
                        messages.error(request, f"Invalid sell quantity for {product.name}. It must be a positive number.")
                except ValueError:
                    messages.error(request, f"Invalid sell quantity for {product.name}. Please enter a valid number.")
                except Exception as e:
                    messages.error(request, str(e))
        messages.success(request, "Quantity stock updated successfully!")
        return redirect('inventory_report')
    return render(request, 'inventory_report.html', {'products': products})

def product(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart(request)
    quantities = cart.get_quants()
    product.quantity = quantities.get(str(product.id), 1)
    related_products = Product.objects.filter(category=product.category).exclude(id=pk)[:4]

    reviews = product.reviews.filter()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                text = review.body.lower()
                if any(word in text for word in ['bad', 'poor', 'worst', 'awful']):
                    review.sentiment = 'Negative'
                elif any(word in text for word in ['good', 'excellent', 'amazing', 'great']):
                    review.sentiment = 'Positive'
                else:
                    review.sentiment = 'Neutral'

                review.save()
                messages.success(request, 'Your review has been submitted for approval.')
                return redirect('product', pk=product.id)
        else:
            messages.error(request, 'You must be logged in to submit a review.')
            return redirect('login')

    else:
        form = ReviewForm()

    return render(request, 'product.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': form,
    })

@staff_member_required
def admin_dashboard(request):
    from django.db.models import Count, Sum
    from django.utils import timezone
    from datetime import timedelta
    from payment.models import Order

    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_reviews = Review.objects.count()

    recent_orders = Order.objects.order_by('-date_ordered')[:5]
    low_stock_products = Product.objects.filter(stock_quantity__lte=5)

    sales_data = []
    visitors_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for month in range(1, 13):
        month_orders = Order.objects.filter(date_ordered__month=month, date_ordered__year=timezone.now().year)
        total_sales = month_orders.aggregate(total=Sum('total_paid'))['total'] or 0
        sales_data.append(float(total_sales))
    
    category_data = Product.objects.values('category__name').annotate(count=Count('id'))
    review_sentiment = {
        'positive': Review.objects.filter(rating__gte=4).count(),
        'neutral': Review.objects.filter(rating=3).count(),
        'negative': Review.objects.filter(rating__lte=2).count(),
    }

    rating_distribution = [
        Review.objects.filter(rating=1).count(),
        Review.objects.filter(rating=2).count(),
        Review.objects.filter(rating=3).count(),
        Review.objects.filter(rating=4).count(),
        Review.objects.filter(rating=5).count(),
    ]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_reviews': total_reviews,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'sales_data': sales_data,
        'months': months,
        'category_data': list(category_data),
        'review_sentiment': review_sentiment,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'admin_dashboard.html', context)
