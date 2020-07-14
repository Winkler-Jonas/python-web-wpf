from django.db import models

# Create your models here.


class Document(models.Model):
    document_name = models.TextField()
    document_path = models.FilePathField(null=True)
    document_date_edit = models.DateTimeField(blank=True, null=True)
    document_date_added = models.DateTimeField(blank=True, null=True)
    document_info = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['document_date_added']
        verbose_name = 'Dokument'
        verbose_name_plural = 'Dokumente'


class DocumentPage(models.Model):
    doc_page_path = models.FilePathField()
    doc_page_no = models.IntegerField()
    doc_fk = models.ForeignKey(Document, related_name='pages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-doc_page_path']
        verbose_name = 'Seite'
        verbose_name_plural = 'Seiten'