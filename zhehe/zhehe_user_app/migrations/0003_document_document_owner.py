# Generated by Django 3.0.3 on 2020-07-19 13:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('zhehe_user_app', '0002_update_site_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_owner',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
