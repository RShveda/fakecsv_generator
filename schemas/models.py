from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.

class Schema(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.CharField(max_length=100, null=True)
    separator = models.CharField(max_length=10, blank=True, null=True)
    string_char = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('schemas:schema_detail', kwargs={'slug': self.slug})


class DataTypes(models.Model):
    """
    Currently supported following types: "name", "job", "email", "integer", "address", "text".
    Must be added via django admin interface.
    """
    type = models.CharField(max_length=80)

    def __str__(self):
        return self.type


class Column(models.Model):
    slug = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=80, unique=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="columns")
    order = models.IntegerField()
    data_type = models.ForeignKey(DataTypes, on_delete=models.CASCADE)
    range_min = models.IntegerField(default=0, blank=True)
    range_max = models.IntegerField(default=0, blank=True)

    class Meta:
        unique_together = ('schema', 'order',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('schemas:schema_detail', kwargs={'slug': self.schema.slug})


class DataSet(models.Model):
    title = models.CharField(max_length=80, blank=True, null=True)
    status = models.CharField(max_length=80, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    url = models.FileField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('schemas:dataset_list')
