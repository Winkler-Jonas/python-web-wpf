from django.db import models

# Create your models here.


class Subscriber(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)


class Contact_Info(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True)
