from django.db import models
from datetime import date

# Create your models here.
class Stock(models.Model):
    itemName = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField()

class Borrow(models.Model):
    itemName = models.CharField(max_length=100)
    quantity = models.IntegerField()
    name = models.CharField(max_length=100)
    regNo = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=50)
    borrowDate = models.CharField(max_length=50, default=date.today())
    returnedDate = models.CharField(max_length=50, default="Not Returned")
    status = models.CharField(max_length=20, default="Not Returned")