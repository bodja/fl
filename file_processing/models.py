import os

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models import signals

from model_utils import Choices

from .tasks import process_file
from .file_processor import FileProcessor


def supplier_directory_path(instance, filename):
    return os.path.join(
        settings.UPLOADS_DIR,
        str(instance.supplier_id),
        filename
    )


class FileModel(models.Model):
    STATUSES = Choices(
        ('pending', 'pending', 'Pending'),
        ('in_progress', 'in_progress', 'In progress'),
        ('success', 'success', 'Success'),
        ('fail', 'fail', 'Fail'),
    )
    file = models.FileField(upload_to=supplier_directory_path)
    supplier_id = models.IntegerField()
    date = models.DateField()
    currency = models.CharField(max_length=5)
    processing_status = models.CharField(max_length=25, choices=STATUSES,
                                         default=STATUSES.pending)

    class Meta(object):
        unique_together = ('supplier_id', 'date', 'currency')

    def can_be_processed(self):
        return self.processing_status == self.STATUSES.pending

    def process(self):
        self.set_status(self.STATUSES.in_progress)

        try:
            FileProcessor(
                supplier_id=self.supplier_id,
                currency=self.currency,
                date=self.date,
                file=self.file
            ).process()
        except Exception as err:
            self.set_status(self.STATUSES.fail)
        else:
            self.set_status(self.STATUSES.success)

    def set_status(self, status):
        self.processing_status = status
        self.save(update_fields=['processing_status'])


@receiver(signals.post_save, sender=FileModel)
def start_processing(sender, instance, **kwargs):
    if instance.can_be_processed():
        process_file.delay(instance.pk)
