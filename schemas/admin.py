from django.contrib import admin
from .models import Schema, Column, DataTypes

# Register your models here.
admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(DataTypes)