from django.contrib import admin

from suppliers.models import Supplier, Customer, Product, Transaction

admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Transaction)
