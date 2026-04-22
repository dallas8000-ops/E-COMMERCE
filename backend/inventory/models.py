
from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
	color = models.CharField(max_length=100, blank=True)
	sizes = models.CharField(max_length=200, help_text='Comma-separated sizes, e.g. S,M,L,XL', blank=True)
	in_stock = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def size_list(self):
		return [s.strip() for s in self.sizes.split(',') if s.strip()]

	def __str__(self):
		return self.name


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='products/')
	alt_text = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return f"Image for {self.product.name}"
