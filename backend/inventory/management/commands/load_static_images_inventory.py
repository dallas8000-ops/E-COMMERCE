from django.core.management.base import BaseCommand
from inventory.models import Category, Product
import os

import os
STATIC_IMAGE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'core', 'static', 'core')
)

class Command(BaseCommand):
    help = 'Load products based on images in static/core/'

    def handle(self, *args, **options):
        cat, _ = Category.objects.get_or_create(name='Default', defaults={'description': 'Default category'})
        image_files = [f for f in os.listdir(STATIC_IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        for img in image_files:
            name = os.path.splitext(img)[0].replace('_', ' ').replace('-', ' ').title()
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'description': '',
                    'price': 20.00,
                    'old_price': 30.00,
                    'category': cat,
                    'color': 'Multicolor',
                    'sizes': 'One Size',
                }
            )
        self.stdout.write(self.style.SUCCESS('Products created for all static images.'))
