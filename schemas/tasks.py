# Create your tasks here
from __future__ import absolute_import, unicode_literals

import time
from celery import shared_task
from .csv_generator import CsvFaker

@shared_task
def add(x, y):
    return x + y

@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 5)
    return True

@shared_task
def make_file_async(schema, rows, pk):
    print("creating file async..")
    url = CsvFaker.make_file(schema, rows, pk)
    print("file created async")
    return True
