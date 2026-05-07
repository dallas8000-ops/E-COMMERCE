from django.db import migrations


def sync_in_stock_flags(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    Product.objects.filter(stock_quantity__gt=0).update(in_stock=True)
    Product.objects.filter(stock_quantity=0).update(in_stock=False)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_product_review'),
    ]

    operations = [
        migrations.RunPython(sync_in_stock_flags, migrations.RunPython.noop),
    ]
