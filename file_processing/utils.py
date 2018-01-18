import datetime
from django.conf import settings


def extract_currency(filename):
    return settings.FILENAME_REGEX.search(filename).group('currency')


def extract_date(filename):
    date = settings.FILENAME_REGEX.search(filename).group('date')
    return datetime.datetime.strptime(date, settings.DATE_FORMAT)
