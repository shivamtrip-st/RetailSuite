from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('checkout/shipping/', views.checkout_shipping, name='checkout_shipping'),
   path('checkout/review/', views.checkout_review, name='checkout_review'),
   path('checkout/complete/', views.checkout_complete, name='checkout_complete'),
   path('payment_success/', views.payment_success, name='payment_success'),
   path('orders/', views.order_history, name='order_history'),
   path('order/<int:order_id>/', views.order_detail, name='order_detail'),
   path('toggle-shipped/<int:order_id>/', views.toggle_shipped_status, name='toggle_shipped_status'),
   path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
   path('success/', views.checkout_success, name='checkout_success'),
   path('cancel/', views.checkout_cancel, name='checkout_cancel'),
]
