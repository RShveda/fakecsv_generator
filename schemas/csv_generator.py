from django.core.files import File
from .models import Schema
import os
from django.conf import settings
from faker import Faker
import csv

class CsvFaker:

    def make_file(schema, rows):
        with open(str(settings.MEDIA_ROOT) + "/datasets/" + schema + str(rows) + ".csv", 'w', newline='') as f:
            myfile = File(f)
            myfile.write(CsvFaker.generate_data(schema, rows))
        myfile.closed
        f.closed
        return myfile.name

    def generate_data(schema, rows):
        schema = Schema.objects.get(name=schema)
        fake = Faker()
        fake.set_arguments('range', {'min_value': 0, 'max_value': 100})
        csv = fake.csv(header=('Name', 'Address', 'Favorite Color'), data_columns=('{{name}}', '{{job}}', '{{pyint:range}}'), num_rows=int(rows), include_row_ids=False)
        return (csv)
