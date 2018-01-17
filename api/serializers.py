from django.conf import settings
from rest_framework import serializers

from api import validators
from file_processing.models import FileModel


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        use_url=False,  # to not have filename as full url in response
        validators=[
            validators.MimeTypeValidator(settings.ALLOWED_MIME_TYPES),
            validators.FileNameValidator(settings.FILENAME_PATTERN)
        ])

    class Meta(object):
        model = FileModel
        fields = [
            'file'
        ]
