# Generated by Django 3.0.8 on 2020-07-21 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zhehe_user_app', '0006_auto_20200720_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_format',
            field=models.CharField(default='rst', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='document_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
