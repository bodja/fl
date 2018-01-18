import re
from rest_framework.exceptions import ValidationError


class MimeTypeValidator(object):
    message = '{mimetype} mime type is not allowed.'
    code = 'not_allowed_mime_type'

    def __init__(self, allowed_types=None):
        self.allowed_types = allowed_types or []

    def __call__(self, uploaded_file):
        if uploaded_file.content_type not in self.allowed_types:
            msg = self.message.format(mimetype=uploaded_file.content_type)
            raise ValidationError(msg, code=self.code)


class RegexValidator(object):
    message = 'Does not match the pattern.'
    code = 'bad_string'
    regex = None

    def __init__(self, regex=None):
        self.regex = regex or self.regex
        retype = type(re.compile(''))
        assert isinstance(self.regex, retype)

    def __call__(self, value):
        if not self.is_valid(value):
            raise ValidationError(self.message, code=self.code)

    def is_valid(self, value):
        return self.regex.search(value)


class FileNameValidator(RegexValidator):
    message = 'File name does not match the pattern.'
    code = 'bad_file_name'

    def is_valid(self, uploaded_file):
        return super(FileNameValidator, self).is_valid(uploaded_file.name)
