import csv
import io
from uuid import uuid4

from django.core.files.base import File
from django.db import transaction
from app.utils import generate_data

from celery import shared_task
from celery.signals import task_failure

from app.models import DataSetTask, Schema


@shared_task
def generate_dataset(schema_pk: int, task_pk: int, rows: int) -> DataSetTask:
    schema = Schema.objects.get(pk=schema_pk)
    task = DataSetTask.objects.get(pk=task_pk)

    with io.StringIO() as file:
        with transaction.atomic():
            filename = f"{str(uuid4())}.csv"
            writer = csv.writer(
                file,
                delimiter=schema.delimiter,
                quotechar=schema.quotechar,
            )
            data = generate_data(schema, rows)
            writer.writerows(data)

            task.file.save(filename, File(file))
            task.status = "ready"
            task.save()
    return task


@task_failure.connect(sender=generate_dataset)
def update_failed_status(
    sender, task_id, exception, args, kwargs, traceback, einfo, **other
):
    _, task_pk, _ = args
    task = DataSetTask.objects.get(pk=task_pk)
    task.status = "failed"
    task.save()
