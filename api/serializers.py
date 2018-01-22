from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from file_processing.models import FileModel
from file_processing.utils import extract_currency, extract_date
from suppliers.models import Transaction
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
        attrs = self.validate_currency(attrs)
        attrs = self.validate_date(attrs)
        attrs = self.validate_supplier_id(attrs)

        self.validate_unique_file(attrs)
        self.validate_unique_transaction(attrs)

        return attrs

    def validate_currency(self, attrs):
        try:
            attrs['currency'] = extract_currency(attrs['file'].name)
        except (AttributeError, IndexError):
            raise serializers.ValidationError('Currency is not recognized.')
        return attrs

    def validate_date(self, attrs):
        try:
            attrs['date'] = extract_date(attrs['file'].name)
        except (AttributeError, IndexError, ValueError):
            raise serializers.ValidationError('Bad date format.')
        return attrs

    def validate_supplier_id(self, attrs):
        attrs['supplier_id'] = self.context['request'].user.id
        return attrs

    def validate_unique_file(self, attrs):
        validator = UniqueTogetherValidator(
            queryset=self.Meta.model.objects.all(),
            fields=('supplier_id', 'date', 'currency')
        )
        validator.set_context(self)
        validator(attrs)

    def validate_unique_transaction(self, attrs):
        validator = UniqueTogetherValidator(
            queryset=Transaction.objects.all(),
            fields=('product__supplier_id', 'delivered', 'customer__currency')
        )
        validator.set_context(self)
        validator({
            'product__supplier_id': attrs['supplier_id'],
            'customer__currency': attrs['currency'],
            'delivered': attrs['date'],
        })
