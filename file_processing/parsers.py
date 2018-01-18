from .file_processor.parsers_registry import register


@register([1, 2])
def dummy_parser(file_instance):
    print(file_instance, type(file_instance))
    return []
