from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
# Register your models here.

admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'total_paid', 'is_shipped', 'shipping_date')
    inlines = [OrderItemInline]
    list_filter = ('is_shipped',)
    search_fields = ('user__username', 'id')

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)