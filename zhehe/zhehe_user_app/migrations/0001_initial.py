# Generated by Django 3.0.3 on 2020-07-15 10:54

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def update_site_name(apps, schema_editor):
    SiteModel = apps.get_model('sites', 'Site')
    domain = 'mydomain.com'

    SiteModel.objects.update_or_create(
        pk=settings.SITE_ID,
        defaults={'domain': domain,
                  'name': domain}
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(update_site_name),
        migrations.CreateModel(
            name='Contact_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('note', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.TextField()),
                ('document_path', models.FilePathField(null=True)),
                ('document_date_edit', models.DateTimeField(blank=True, null=True)),
                ('document_date_added', models.DateTimeField(blank=True, null=True)),
                ('document_info', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Dokument',
                'verbose_name_plural': 'Dokumente',
                'ordering': ['document_date_added'],
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_page_path', models.FilePathField()),
                ('doc_page_no', models.IntegerField()),
                ('doc_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='zhehe_user_app.Document')),
            ],
            options={
                'verbose_name': 'Seite',
                'verbose_name_plural': 'Seiten',
                'ordering': ['-doc_page_path'],
            },
        ),
    ]
