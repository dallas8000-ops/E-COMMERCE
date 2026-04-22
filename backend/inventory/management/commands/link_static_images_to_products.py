import os
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from inventory.models import Product, ProductImage


COMMAND_DIR = Path(__file__).resolve().parent
BACKEND_DIR = COMMAND_DIR.parents[2]
WORKSPACE_DIR = BACKEND_DIR.parent
IMAGE_DIRECTORIES = [
    WORKSPACE_DIR / 'images',
    BACKEND_DIR / 'core' / 'static' / 'core',
]
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')


class Command(BaseCommand):
    help = 'Link uploaded catalog images to products as ProductImage entries.'

    def normalize(self, s):
        return ''.join(e for e in s.lower() if e.isalnum())

    def get_image_files(self):
        image_files = {}
        for directory in IMAGE_DIRECTORIES:
            if not directory.exists():
                continue

            for file_path in directory.iterdir():
                if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

                image_files.setdefault(self.normalize(file_path.stem), file_path)

        return image_files

    def handle(self, *args, **options):
        normalized_files = self.get_image_files()

        if not normalized_files:
            self.stdout.write(self.style.WARNING('No catalog images found in images/ or backend/core/static/core/.'))
            return

        for product in Product.objects.all():
            norm_name = self.normalize(product.name)
            image_path = normalized_files.get(norm_name)
            if image_path:
                fname = image_path.name
                # Link image as ProductImage if not already linked
                if not product.images.filter(image='products/' + fname).exists():
                    # Copy image to media/products/
                    dest_path = BACKEND_DIR / 'media' / 'products' / fname
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(image_path, 'rb') as src, open(dest_path, 'wb') as dst:
                        dst.write(src.read())
                    # Save ProductImage
                    with open(dest_path, 'rb') as img_file:
                        ProductImage.objects.create(product=product, image=File(img_file, name='products/' + fname))
                self.stdout.write(self.style.SUCCESS(f'Linked image for product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'No image found for product: {product.name}'))
        self.stdout.write(self.style.SUCCESS('Linked images to products.'))
