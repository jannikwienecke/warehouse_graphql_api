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
    packaging = models.ForeignKey('warehouse.Packaging', on_delete=models.CASCADE)
    
class Packaging(models.Model):
    name = models.CharField(max_length=50)
    width = models.IntegerField()
    length = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Employee(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    width = models.IntegerField()
    length = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Customer(models.Model):
    customer_id = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Symfactory(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Symbuilding(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symfactory = models.ForeignKey('warehouse.Symfactory', on_delete=models.CASCADE)

class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Compartment(models.Model):
    name = models.CharField(max_length=50)
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    position_top = models.IntegerField()
    position_left = models.IntegerField()
    real_position = models.CharField(max_length=50)
    direction = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Row(models.Model):
    name = models.CharField(max_length=50)
    stock = models.IntegerField(null=True, default=0)
    stock_positions = models.IntegerField(null=True, default=0)
    number_stock_positions = models.IntegerField()
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    compartment = models.ForeignKey('warehouse.Compartment', on_delete=models.CASCADE)
    product = models.ForeignKey('warehouse.Product', blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Tour(models.Model):
    name = models.CharField(max_length=50)
    is_open = models.BooleanField(default=True)
    tour_number = models.IntegerField()
    employee = models.ForeignKey('warehouse.Employee', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('warehouse.Vehicle', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Withdrawal(models.Model):
    name  = models.CharField(max_length=50)
    tour = models.ForeignKey('warehouse.Tour', on_delete=models.CASCADE)
    employee = models.ForeignKey('warehouse.Employee', on_delete=models.CASCADE)
    product = models.ForeignKey('warehouse.Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('warehouse.Customer', on_delete=models.CASCADE)
    row = models.ForeignKey('warehouse.Row', on_delete=models.CASCADE)
    notes = models.TextField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)




