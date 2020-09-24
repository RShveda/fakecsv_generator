from django.contrib import admin
from .models import Schema, Column, DataTypes, DataSet

# Register your models here.
admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(DataTypes)
admin.site.register(DataSet)