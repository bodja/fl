from file_processing.file_processor.parsers_registry import get_parser


class FileProcessor(object):

    def __init__(self, supplier_id, currency, date, file):
        self.supplier_id = supplier_id
        self.currency = currency
        self.date = date
        self.file = file

    def parse(self):
        """
        :return: list should return a result to be used in post_parse
        """
        return get_parser(self.supplier_id)(self.file)

    def process(self):
        result = self.parse()
        self.save(result)

    def save(self, data):
        # TODO
        raise NotImplementedError
