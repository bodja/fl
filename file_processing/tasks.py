from celery import shared_task


@shared_task
def process_file(pk):
    from .models import FileModel

    FileModel.objects.get(pk=pk).process()
