from django.db import migrations


class Migration(migrations.Migration):
    """Placeholder — group creation moved to admin setup (avoid migration timing issues)."""

    dependencies = [
        ('core', '0001_staff_portal_config'),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop, migrations.RunPython.noop),
    ]
