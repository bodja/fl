from rest_framework import mixins, viewsets

from file_processing.models import FileModel
from . import serializers, authentication, permissions


class FileUploadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = FileModel
    serializer_class = serializers.FileUploadSerializer
    queryset = FileModel.objects.all()
    authentication_classes = (
        authentication.SupplierAuthentication,
    )
    permission_classes = (
        permissions.SupplierIsAuthenticated,
    )
