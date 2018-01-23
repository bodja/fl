__all__ = ['register', 'get_parser']

REGISTERED_PARSERS = {}


def _register(supplier_id, func):
    if supplier_id in REGISTERED_PARSERS:
        raise ValueError(
            f'Another parser for supplier_id={supplier_id} was already '
            f'registered {func.__name__}.'
        )
    REGISTERED_PARSERS[supplier_id] = func


def register(supplier_ids):
    """
    @register(123)
    def my_parser(file_instance):
        ...
        do you parsing magic
        ...
        return parsed_data
    """
    if not isinstance(supplier_ids, (list, tuple, set)):
        supplier_ids = [supplier_ids]

    def wrapper(func):
        for supplier_id in supplier_ids:
            _register(supplier_id, func)
        return func

    return wrapper


def get_parser(supplier_id):
    if supplier_id not in REGISTERED_PARSERS:
        msg = f'Parser for supplier_id={supplier_id} is not registered.'
        raise ValueError(msg)

    return REGISTERED_PARSERS[supplier_id]
