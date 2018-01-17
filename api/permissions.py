from rest_framework.permissions import BasePermission

from suppliers.models import Supplier


class SupplierIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return isinstance(request.user, Supplier)
