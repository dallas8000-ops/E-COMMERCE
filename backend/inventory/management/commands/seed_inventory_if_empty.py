from pathlib import Path
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.core.management import call_command
from django.core.management.base import BaseCommand

from inventory.models import Category, Product


DEFAULT_SIZE_RANGE = '32,34,36,38,40,42,44,46,48,50,52,54'
DEFAULT_UGX_RATE = Decimal('3700')


class Command(BaseCommand):
    help = 'Load inventory seed data when the product table is empty.'

    @staticmethod
    def _to_decimal(value, default='0'):
        try:
            return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except (InvalidOperation, TypeError, ValueError):
            return Decimal(default).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def _seed_categories_from_rows(self, rows):
        for row in rows:
            fields = row.get('fields', {})
            Category.objects.update_or_create(
                pk=row.get('pk'),
                defaults={
                    'name': fields.get('name') or 'Default',
                    'description': fields.get('description') or '',
                },
            )

    def _product_defaults_from_legacy_fields(self, fields):
        usd_price = self._to_decimal(fields.get('price_usd') or fields.get('price') or '0')
        ugx_price = (usd_price * DEFAULT_UGX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        old_price_raw = fields.get('old_price')
        old_price = self._to_decimal(old_price_raw) if old_price_raw not in (None, '') else None
        in_stock = bool(fields.get('in_stock', True))
        stock_quantity = max(0, int(fields.get('stock_quantity') or 1))
        if not in_stock:
            stock_quantity = 0

        return {
            'name': fields.get('name') or 'Catalog Item',
            'description': fields.get('description') or '',
            'price_usd': usd_price,
            'price_ugx': ugx_price,
            'old_price': old_price,
            'category_id': fields.get('category'),
            'color': fields.get('color') or '',
            'sizes': DEFAULT_SIZE_RANGE,
            'in_stock': in_stock,
            'stock_quantity': stock_quantity,
        }

    def _seed_products_from_rows(self, rows):
        for row in rows:
            fields = row.get('fields', {})
            Product.objects.update_or_create(
                pk=row.get('pk'),
                defaults=self._product_defaults_from_legacy_fields(fields),
            )

    def _seed_from_legacy_fixture(self, fixture_path: Path):
        raw = json.loads(fixture_path.read_text(encoding='utf-8'))
        category_rows = [row for row in raw if row.get('model') == 'inventory.category']
        product_rows = [row for row in raw if row.get('model') == 'inventory.product']

        self._seed_categories_from_rows(category_rows)
        self._seed_products_from_rows(product_rows)

    def handle(self, *args, **options):
        existing_count = Product.objects.count()
        if existing_count:
            self.stdout.write(self.style.SUCCESS(f'Skipping inventory seed; {existing_count} products already exist.'))
            return

        fixture_path = Path(__file__).resolve().parents[3] / 'fixtures' / 'inventory_seed.json'
        if not fixture_path.exists():
            self.stdout.write(self.style.ERROR(f'Inventory seed fixture not found: {fixture_path}'))
            raise SystemExit(1)

        try:
            call_command('loaddata', str(fixture_path))
        except Exception as exc:
            self.stdout.write(self.style.WARNING(
                f'Fixture load failed with schema mismatch ({exc}). Falling back to legacy seed parser.'
            ))
            self._seed_from_legacy_fixture(fixture_path)

        Product.objects.update(sizes=DEFAULT_SIZE_RANGE)
        seeded_count = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Inventory seed complete; {seeded_count} products loaded.'))
