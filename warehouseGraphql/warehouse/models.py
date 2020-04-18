from django.db import models
from django.conf import settings


class Product(models.Model) :
    product_number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    notes_picking = models.TextField(blank=True, null=True)
    notes_putaway = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    three_in_row = models.BooleanField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    packaging = models.ForeignKey('warehouse.Packaging', related_name='products', on_delete=models.CASCADE)
    
class Packaging(models.Model):
    name = models.CharField(max_length=50)
    width = models.IntegerField()
    length = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Employee(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)