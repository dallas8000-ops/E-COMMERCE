

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
	model = CartItem
	extra = 1

class CartAdmin(admin.ModelAdmin):
	inlines = [CartItemInline]
	list_display = ('id', 'user', 'session_key', 'created_at')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ('product_name', 'quantity', 'size', 'color', 'unit_price', 'line_total')
	can_delete = False


class OrderAdmin(admin.ModelAdmin):
	list_display = ('order_ref', 'customer_name', 'phone', 'country', 'payment_method', 'currency', 'total_amount', 'status', 'created_at')
	list_filter = ('status', 'payment_method', 'currency', 'created_at')
	search_fields = ('order_ref', 'customer_name', 'phone')
	readonly_fields = ('order_ref', 'created_at')
	inlines = [OrderItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
