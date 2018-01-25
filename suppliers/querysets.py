from django.db import transaction
from django.db.models import QuerySet
import logging

logger = logging.getLogger(__name__)

class SupplierQuerySet(QuerySet):

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class TransactionQuerySet(QuerySet):

    @transaction.atomic  # commit in single transaction, rollback on exception
    def update_or_create_from_data(self, supplier_id, currency, date, data):
        """
        :param supplier_id: <int> id of the supplier record
        :param currency: <str> currency code
        :param date: <datetime> or date ISO format
        :param data: <list> of <dict>. List of transactions
            [
                {
                    "customer_code": "AAA1",
                    "customer_title": "Example Customer",
                    "product_code": "000A",
                    "product_title": "Example Product",
                    "delivered": "2017-12-01",
                    "cost": 1.11,
                    "quantity": 2.22,
                    "price": 3.33
                },
                ...
            ]
        """
        from .models import Customer, Product  # to avoid circular import
        from django.utils import timezone
        from datetime import datetime

        dt_unaware = datetime.combine(date, datetime.min.time())
        dt_aware = timezone.make_aware(dt_unaware, timezone.get_current_timezone())
        for trans in data:
            # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#update-or-create
            # "defaults" are fields to be updated with provided values
            try:
                customer, created = Customer.objects.update_or_create(
                    supplier_id=supplier_id,
                    code=trans['customer_code'],
                    currency=currency,
                    defaults={'title': trans['customer_title']}
                )

                product, created = Product.objects.update_or_create(
                    supplier_id=supplier_id,
                    code=trans['customer_code'],
                    defaults={'title': trans['customer_title']}
                )

                self.model.objects.create(
                    customer=customer,
                    product=product,
                    delivered=dt_aware,
                    cost=trans['cost'],
                    quantity=trans['quantity'],
                    price=trans['price']
                )
            except Exception as e:
                logger.exception(str(e))
