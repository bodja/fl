from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.conf import settings

from .querysets import SupplierQuerySet, TransactionQuerySet


class Supplier(models.Model):
    objects = SupplierQuerySet.as_manager()
    USERNAME_FIELD = 'code'

    code = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'suppliers'
        managed = settings.SUPPLIERS_TABLES_MANAGED

    def __str__(self):
        return f'{self.code}:{self.title}'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Customer(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255)
    last_delivered = models.DateTimeField(null=True)
    month_value = models.FloatField(null=True)
    threatened_value = models.FloatField(null=True)
    growth = models.FloatField(null=True)

    class Meta(object):
        db_table = 'customers'
        managed = settings.SUPPLIERS_TABLES_MANAGED

    def __str__(self):
        return f'{self.code}:{self.currency}:{self.title}'


class Product(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'products'
        managed = settings.SUPPLIERS_TABLES_MANAGED

    def __str__(self):
        return f'{self.code}:{self.title}'


class Transaction(models.Model):
    objects = TransactionQuerySet.as_manager()

    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    cost = models.FloatField(null=True)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    delivered = models.DateTimeField()
    stopped = models.BooleanField()

    class Meta(object):
        db_table = 'transactions'
        managed = settings.SUPPLIERS_TABLES_MANAGED

    def __str__(self):
        return f'{self.product} - {self.delivered}'
