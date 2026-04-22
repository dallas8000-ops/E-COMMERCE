

from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'in_stock')
	list_filter = ('category', 'in_stock')
	search_fields = ('name', 'description')
	inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
