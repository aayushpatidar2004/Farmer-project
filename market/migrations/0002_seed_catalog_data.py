from django.core.management import call_command
from django.db import migrations


def seed_shared_catalogs(apps, schema_editor):
    """Populate shared disease and market demo catalogs during deployment."""
    call_command('load_sample_data', catalog_only=True, verbosity=0)


class Migration(migrations.Migration):
    dependencies = [
        ('diseases', '0001_initial'),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_shared_catalogs, migrations.RunPython.noop),
    ]
