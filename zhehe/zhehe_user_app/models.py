from django.db import models

# Create your models here.


class Subscriber(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)


class Contact_Info(models.Model):
    concern = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True)


class Document(models.Model):
    document_owner = models.IntegerField()
    document_name = models.TextField()
    document_path = models.CharField(max_length=500, primary_key=True)
    document_text = models.TextField()
    document_format = models.CharField(max_length=5)
    document_date_edit = models.DateTimeField(blank=True, null=True)
    document_date_added = models.DateTimeField(blank=True, null=True)
    document_info = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['document_date_added']
        verbose_name = 'Dokument'
        verbose_name_plural = 'Dokumente'


class DocumentPage(models.Model):
    doc_page_path = models.CharField(max_length=500, primary_key=True)
    doc_page_no = models.IntegerField()
    doc_fk = models.ForeignKey(Document, related_name='pages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-doc_page_path']
        verbose_name = 'Seite'
        verbose_name_plural = 'Seiten'