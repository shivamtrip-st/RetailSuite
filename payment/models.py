from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from store.models import Product
from django.contrib.auth.models import User
import datetime

class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_full_name = models.CharField(max_length=255)
	shipping_email = models.CharField(max_length=255)
	shipping_address1 = models.CharField(max_length=255)
	shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
	shipping_city = models.CharField(max_length=255)
	shipping_state = models.CharField(max_length=255, null=True, blank=True)
	shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
	shipping_country = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "Shipping Address"

	def __str__(self):
		return f'Shipping Address - {str(self.id)}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    shipping_date = models.DateTimeField(blank=True, null=True)
    is_shipped = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_shipped and not self.shipping_date:
            self.shipping_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
