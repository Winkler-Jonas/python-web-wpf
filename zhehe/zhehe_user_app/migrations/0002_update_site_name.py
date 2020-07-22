# Generated by Django 3.0.3 on 2020-07-17 14:37

from django.db import migrations
from django.conf import settings


def update_site_name(apps, schema_editor):
    SiteModel = apps.get_model('sites', 'Site')
    domain = 'zhehe.com'

    SiteModel.objects.update_or_create(
        pk=settings.SITE_ID,
        defaults={'domain': domain,
                  'name': 'Zhehe'}
    )


class Migration(migrations.Migration):

    dependencies = [
        ('zhehe_user_app', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(update_site_name),
    ]