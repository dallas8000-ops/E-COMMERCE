

from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
	model = CartItem
	extra = 1

class CartAdmin(admin.ModelAdmin):
	inlines = [CartItemInline]
	list_display = ('id', 'user', 'session_key', 'created_at')

admin.site.register(Cart, CartAdmin)
