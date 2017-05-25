from django.db import migrations

def create_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.create(name='Incube dev', domain='localhost')
    Site.objects.create(name='Incube', domain='incube.io')

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_sites)
    ]
