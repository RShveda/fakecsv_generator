# Generated by Django 3.1.1 on 2021-04-25 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0015_auto_20210418_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='slug',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
