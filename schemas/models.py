from django.db import models

# Create your models here.

class Schema(models.Model):
    name = models.CharField(max_length=80)
    separator = models.CharField(max_length=10, blank=True, null=True)
    string_char = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataTypes(models.Model):
    type = models.CharField(max_length=80)
    range_min = models.IntegerField()
    range_max = models.IntegerField()

    def __str__(self):
        return self.type


class Column(models.Model):
    name = models.CharField(max_length=80)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="columns")
    order = models.IntegerField(unique=True)
    data_types = models.ManyToManyField(DataTypes)

    def __str__(self):
        return self.name

