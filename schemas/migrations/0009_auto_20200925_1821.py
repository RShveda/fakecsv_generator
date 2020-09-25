# Generated by Django 3.1.1 on 2020-09-25 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0008_auto_20200925_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='data_types',
        ),
        migrations.AddField(
            model_name='column',
            name='data_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='schemas.datatypes'),
            preserve_default=False,
        ),
    ]
