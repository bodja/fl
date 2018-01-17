from suppliers.models import Supplier


def authenticate(request, username=None, password=None, **kwargs):
    if username is None:
        username = kwargs.get(Supplier.USERNAME_FIELD)
    try:
        user = Supplier.objects.get_by_natural_key(username)
    except Supplier.DoesNotExist:
        pass
    else:
        if user.check_password(password):
            return user
