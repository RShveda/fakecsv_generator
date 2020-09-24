from django.core.files import File
import os
from django.conf import settings

class CsvFaker:

    def make_file(schema, rows):
        with open(str(settings.MEDIA_ROOT) + "\datasets\\" + schema + str(rows) + ".txt", 'w') as f:
            myfile = File(f)
            myfile.write('Hello World ' + schema)
        myfile.closed
        f.closed
        return myfile.name

    def generate_data(self):
        pass