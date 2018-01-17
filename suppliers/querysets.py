from django.db.models import QuerySet


class SupplierQueryset(QuerySet):

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
