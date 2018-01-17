from django.db import models
from django.conf import settings


class FileModel(models.Model):
    file = models.FileField(upload_to=settings.UPLOADS_DIR)
