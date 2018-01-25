from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_file(pk):
    from .models import FileModel

    logger.info('Pulling new task from celery queue')
    FileModel.objects.get(pk=pk).process()
