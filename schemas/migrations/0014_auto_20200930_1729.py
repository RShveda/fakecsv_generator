# Generated by Django 3.1.1 on 2020-09-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0013_auto_20200930_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='range_max',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='column',
            name='range_min',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
