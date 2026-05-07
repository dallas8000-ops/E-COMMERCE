from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Category, Product


class InventoryApiSmokeTests(APITestCase):
	def setUp(self):
		self.category = Category.objects.create(name='Shirts', description='Top wear')
		Product.objects.create(
			name='Classic Tee',
			description='Cotton t-shirt',
			price_usd=Decimal('19.99'),
			price_ugx=Decimal('73963.00'),
			category=self.category,
			in_stock=True,
		)

	def test_products_endpoint_returns_ok_and_data(self):
		response = self.client.get(reverse('product-list'))
		self.assertEqual(response.status_code, 200)
		self.assertGreaterEqual(len(response.data), 1)

	def test_categories_endpoint_returns_ok_and_data(self):
		response = self.client.get(reverse('category-list'))
		self.assertEqual(response.status_code, 200)
		self.assertGreaterEqual(len(response.data), 1)

	def test_anonymous_cannot_create_category(self):
		response = self.client.post(
			reverse('category-list'),
			data={'name': 'Unauthorized', 'description': 'x'},
			format='json',
		)
		self.assertEqual(response.status_code, 403)

	def test_authenticated_shopper_cannot_create_category(self):
		User = get_user_model()
		user = User.objects.create_user('shopper', password='StrongShopperPass123!')
		self.client.force_login(user)
		response = self.client.post(
			reverse('category-list'),
			data={'name': 'HackerCat', 'description': 'x'},
			format='json',
		)
		self.assertEqual(response.status_code, 403)

	def test_staff_can_create_category(self):
		User = get_user_model()
		staff = User.objects.create_user(
			'staff_api',
			password='StrongStaffPass123!',
			is_staff=True,
		)
		self.client.force_login(staff)
		response = self.client.post(
			reverse('category-list'),
			data={'name': 'Staff Category', 'description': 'Created via API'},
			format='json',
		)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(Category.objects.filter(name='Staff Category').count(), 1)

	def test_product_accepts_eu_sizes_only(self):
		product = Product(
			name='Tailored Dress',
			description='Structured silhouette',
			price_usd=Decimal('39.99'),
			price_ugx=Decimal('147963.00'),
			category=self.category,
			sizes='32, 38, EU 44, 54',
		)

		product.full_clean()
		product.clean()
		self.assertEqual(product.sizes, '32,38,44,54')

	def test_product_rejects_non_eu_sizes(self):
		product = Product(
			name='Tailored Dress',
			description='Structured silhouette',
			price_usd=Decimal('39.99'),
			price_ugx=Decimal('147963.00'),
			category=self.category,
			sizes='S,M,L',
		)

		with self.assertRaises(ValidationError):
			product.full_clean()

	def test_partial_save_writes_in_stock_when_only_stock_quantity_updated(self):
		p = Product.objects.create(
			name='Qty Sync Shirt',
			description='Stock flag sync test',
			price_usd=Decimal('12.00'),
			price_ugx=Decimal('44400.00'),
			category=self.category,
			sizes='32,34',
			stock_quantity=0,
		)
		p.refresh_from_db()
		self.assertFalse(p.in_stock)
		p.stock_quantity = 4
		p.save(update_fields=['stock_quantity'])
		p.refresh_from_db()
		self.assertTrue(p.in_stock)
		self.assertEqual(p.stock_quantity, 4)
