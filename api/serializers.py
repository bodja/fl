from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from file_processing.models import FileModel
from file_processing.utils import extract_currency, extract_date
from . import validators


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        use_url=False,  # to not have filename as full url in response
        validators=[
            validators.MimeTypeValidator(settings.ALLOWED_MIME_TYPES),
            validators.FileNameValidator(settings.FILENAME_REGEX)
        ])

    class Meta(object):
        model = FileModel
        fields = [
            'file'
        ]

    def validate(self, attrs):
        filename = attrs['file'].name

        try:
            attrs['currency'] = extract_currency(filename)
        except (AttributeError, IndexError):
            raise serializers.ValidationError('Currency is not recognized.')

        try:
            attrs['date'] = extract_date(filename)
        except (AttributeError, IndexError, ValueError):
            raise serializers.ValidationError('Bad date format.')

        attrs['supplier_id'] = self.context['request'].user.id

        self.validate_unique_together(attrs)

        return attrs

    def validate_unique_together(self, attrs):
        validator = UniqueTogetherValidator(
            queryset=self.Meta.model.objects.all(),
            fields=('supplier_id', 'date', 'currency')
        )
        validator.set_context(self)
        validator(attrs)
