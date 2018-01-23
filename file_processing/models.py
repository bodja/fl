import os
import logging

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models import signals

from model_utils import Choices

from suppliers.models import Transaction
from .tasks import process_file
from .parsers_registry import get_parser

# Get an instance of a logger
logger = logging.getLogger(__name__)


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

    def __str__(self):
        return f'{self.get_processing_status_display()}:' \
               f'{self.supplier_id}-{self.currency}-{self.date}'

    def can_be_processed(self):
        return self.processing_status == self.STATUSES.pending

    def process(self):
        self.set_status(self.STATUSES.in_progress)

        try:
            parser = get_parser(self.supplier_id)
            data = parser(self.file)
            Transaction.objects.update_or_create_from_data(data)

        except Exception:  # todo: specify exact exceptions
            self.set_status(self.STATUSES.fail)
            logger.exception('Failed to process the file %s.', self.file.name)
        else:
            self.set_status(self.STATUSES.success)

    def set_status(self, status):
        self.processing_status = status
        self.save(update_fields=['processing_status'])


@receiver(signals.post_save, sender=FileModel)
def start_processing(sender, instance, **kwargs):
    if instance.can_be_processed():
        process_file.delay(instance.pk)
