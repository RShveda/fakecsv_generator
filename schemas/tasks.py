# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .csv_generator import CsvFaker


@shared_task
def make_file_async(schema, rows, pk):
    CsvFaker.make_file(schema, rows, pk)
    print("file created async")
    return True
