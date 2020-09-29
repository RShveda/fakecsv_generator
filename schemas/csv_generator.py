from django.core.files import File
from .models import Schema, DataSet
import os
from django.conf import settings
from faker import Faker
from celery import shared_task
import cloudinary.uploader

class CsvFaker:

    @shared_task
    def make_file(schema, rows, pk):
        with open(str(settings.MEDIA_ROOT) + "/datasets/buffer" + ".csv", 'w', newline='') as myfile:
            # myfile = File(f)
            myfile.write(CsvFaker.generate_data(schema, rows))
        myfile.closed
        # f.closed
        uploaded_file = cloudinary.uploader.upload(myfile.name, resource_type="raw", public_id=schema + str(rows))
        print (uploaded_file["secure_url"])
        print(pk)
        print(myfile.name)
        # print(myfile.file.name)
        new_data = DataSet.objects.get(pk=pk)
        new_data.status = "ready"
        # new_data.url = "media/datasets/" + os.path.basename(myfile.file.name)
        new_data.url = uploaded_file["secure_url"]
        new_data.save()
        return new_data.url

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

