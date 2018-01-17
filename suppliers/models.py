from django.db import models
from django.conf import settings


class Supplier(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'suppliers'
        managed = settings.DEBUG  # for development mode when no database


class Customer(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255)
    last_delivered = models.DateTimeField(null=True)  # todo: check maybe it's TimeField
    month_value = models.FloatField(null=True)
    threatened_value = models.FloatField(null=True)
    growth = models.FloatField(null=True)

    class Meta(object):
        db_table = 'customers'
        managed = settings.DEBUG


class Product(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'products'
        managed = settings.DEBUG


class Transactions(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    cost = models.FloatField(null=True)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    delivered = models.DateTimeField()  # todo: check maybe it's TimeField
    stopped = models.BooleanField()

    class Meta(object):
        db_table = 'transactions'
        managed = settings.DEBUG
