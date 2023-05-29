from django.db import models

# Create your models here.
class Table(models.Model):
    name = models.CharField(default="Name", max_length=100)