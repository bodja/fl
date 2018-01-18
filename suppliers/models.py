from django.db import models
from django.conf import settings

from suppliers.querysets import SupplierQueryset


class Supplier(models.Model):
    objects = SupplierQueryset.as_manager()
    USERNAME_FIELD = 'code'

    code = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'suppliers'
        managed = settings.DATABASES['suppliers_db']['TABLES_MANAGED']

    def check_password(self, password):
        # TODO
        return password == password


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
        managed = settings.DATABASES['suppliers_db']['TABLES_MANAGED']


class Product(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'products'
        managed = settings.DATABASES['suppliers_db']['TABLES_MANAGED']


class Transactions(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    cost = models.FloatField(null=True)
    price = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    delivered = models.DateTimeField()
    stopped = models.BooleanField()

    class Meta(object):
        db_table = 'transactions'
        managed = settings.DATABASES['suppliers_db']['TABLES_MANAGED']
