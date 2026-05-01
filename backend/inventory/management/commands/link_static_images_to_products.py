import os
from pathlib import Path
import re
import shutil

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
MEDIA_ROOT = BACKEND_DIR / 'media'
MEDIA_PRODUCTS_DIR = MEDIA_ROOT / 'products'
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
DJANGO_IMAGE_SUFFIX_RE = re.compile(r'^(?P<stem>.+)_[A-Za-z0-9]{7}$')


class Command(BaseCommand):
    help = 'Link uploaded catalog images to products as ProductImage entries.'

    def normalize(self, s):
        return ''.join(e for e in s.lower() if e.isalnum())

    def strip_django_suffix(self, stem):
        match = DJANGO_IMAGE_SUFFIX_RE.match(stem)
        return match.group('stem') if match else stem

    def media_relative_name(self, file_path):
        return file_path.relative_to(MEDIA_ROOT).as_posix()

    def ensure_media_copy(self, source_path):
        if source_path.is_relative_to(MEDIA_ROOT):
            return source_path

        dest_path = MEDIA_PRODUCTS_DIR / source_path.name
        os.makedirs(dest_path.parent, exist_ok=True)
        if not dest_path.exists():
            shutil.copyfile(source_path, dest_path)
        return dest_path

    def iter_media_files(self):
        if not MEDIA_ROOT.exists():
            return

        for file_path in MEDIA_ROOT.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield file_path

    def iter_source_files(self):
        for directory in IMAGE_DIRECTORIES:
            if not directory.exists():
                continue

            for file_path in directory.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    yield file_path

    def index_file(self, image_files, file_path):
        for stem in {file_path.stem, self.strip_django_suffix(file_path.stem)}:
            image_files.setdefault(self.normalize(stem), file_path)

    def get_image_files(self):
        image_files = {}

        for file_path in self.iter_media_files() or []:
            self.index_file(image_files, file_path)

        for file_path in self.iter_source_files():
            self.index_file(image_files, file_path)

        return image_files

    def reconcile_product_image(self, product_image, image_path):
        media_path = self.ensure_media_copy(image_path)
        image_name = self.media_relative_name(media_path)
        if product_image.image.name != image_name:
            product_image.image.name = image_name
            product_image.save(update_fields=['image'])
            return True
        return False

    def normalize_existing_images(self, product, image_path):
        updated_count = 0
        for product_image in product.images.all():
            if self.reconcile_product_image(product_image, image_path):
                updated_count += 1
        return updated_count

    def create_product_image(self, product, image_path):
        dest_path = self.ensure_media_copy(image_path)
        with open(dest_path, 'rb') as img_file:
            ProductImage.objects.create(
                product=product,
                image=File(img_file, name=self.media_relative_name(dest_path)),
            )

    def handle_product(self, product, normalized_files):
        norm_name = self.normalize(product.name)
        image_path = normalized_files.get(norm_name)
        if not image_path:
            self.stdout.write(self.style.WARNING(f'No image found for product: {product.name}'))
            return

        if product.images.exists():
            updated_count = self.normalize_existing_images(product, image_path)
            if updated_count:
                self.stdout.write(self.style.SUCCESS(f'Normalized {updated_count} image record(s) for product: {product.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Image already linked for product: {product.name}'))
            return

        self.create_product_image(product, image_path)
        self.stdout.write(self.style.SUCCESS(f'Linked image for product: {product.name}'))

    def handle(self, *args, **options):
        normalized_files = self.get_image_files()

        if not normalized_files:
            self.stdout.write(self.style.WARNING('No catalog images found in media/, images/, or backend/core/static/core/.'))
            return

        for product in Product.objects.all():
            self.handle_product(product, normalized_files)

        self.stdout.write(self.style.SUCCESS('Linked images to products.'))
