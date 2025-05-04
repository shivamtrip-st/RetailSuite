from django.contrib import admin
from .models import Category, Customer, Order, Product, Profile, Review
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)

class ProfileInline(admin.StackedInline):
	model = Profile

class UserAdmin(admin.ModelAdmin):
	model = User
	fields = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock_quantity', 'sold_quantity', 'is_in_stock']
    list_filter = ['is_in_stock']
    search_fields = ['name', 'description']
    ordering = ['name']
    actions = ['restock_inventory']

    def restock_inventory(self, request, queryset):
        for product in queryset:
            product.restock(10)  # Restocks 10 units for each selected product
            self.message_user(request, f"Restocked {product.name} by 10 units.")
    restock_inventory.short_description = "Restock selected products by 10 units"

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'user', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating', 'created_at')
    search_fields = ('title', 'body', 'user__username', 'product__name')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)
