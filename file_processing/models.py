import os
from django.db import models
from django.conf import settings


def supplier_directory_path(instance, filename):
    return os.path.join(
        settings.UPLOADS_DIR,
        str(instance.supplier_id),
        filename
    )


class FileModel(models.Model):
    file = models.FileField(upload_to=supplier_directory_path)
    supplier_id = models.IntegerField()
    date = models.DateField()
    currency = models.CharField(max_length=5)

    class Meta(object):
        unique_together = ('supplier_id', 'date', 'currency')
