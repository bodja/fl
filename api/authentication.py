from rest_framework import authentication
from rest_framework import exceptions

from suppliers.auth import authenticate
from suppliers.models import Supplier


class SupplierAuthentication(authentication.BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        credentials = {
            Supplier.USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username/password.')

        return user, None
