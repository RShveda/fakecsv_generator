from django.core.files import File
from .models import Schema
import os
from django.conf import settings
from faker import Faker
from celery import shared_task

class CsvFaker:

    @shared_task
    def make_file(schema, rows, new_data):
        with open(str(settings.MEDIA_ROOT) + "/datasets/" + schema + str(rows) + ".csv", 'w', newline='') as f:
            myfile = File(f)
            myfile.write(CsvFaker.generate_data(schema, rows))
        myfile.closed
        f.closed
        new_data.status = "uploaded"
        new_data.url = "media/datasets\\"+ os.path.basename(myfile.file.name)
        new_data.save()
        print("file created")
        return myfile.name

    def generate_data(schema, rows):
        schema = Schema.objects.get(name=schema)
        columns = schema.columns.order_by("order")
        fake = Faker()
        header, data_columns = CsvFaker.serialize(columns, fake)
        csv = fake.csv(header=header, data_columns=data_columns, num_rows=int(rows), include_row_ids=False)
        return (csv)

    def serialize(columns, fake):
        """
        This method formats data according to faker csv(dsv) data format described here:
        https://faker.readthedocs.io/en/master/providers/faker.providers.misc.html#faker.providers.misc.Provider.dsv
        :param fake - faker object that will be generating fake data
        :return:
        """
        header = []
        data_columns = []
        for idx, column in enumerate(columns):
            header.append(column.name)
            if (column.range_min and column.range_max) is not None:
                print(column.data_type)
                if str(column.data_type) == "integer":
                    data_columns.append("{{pyint:range" + str(idx) + "}}")
                    fake.set_arguments('range' + str(idx),
                                       {'min_value': column.range_min, 'max_value': column.range_max})
                elif str(column.data_type) == "text":
                    data_columns.append("{{paragraph:range" + str(idx) + "}}")
                    fake.set_arguments('range' + str(idx),
                                       {'nb_sentences': (column.range_max+column.range_min)/2})
                else:
                    # format not supported
                    data_columns.append("{{" + str(column.data_type) + "}}")
            else:
                data_columns.append("{{" + str(column.data_type) + "}}")
        return (tuple(header), tuple(data_columns))

