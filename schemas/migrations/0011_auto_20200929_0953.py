# Generated by Django 3.1.1 on 2020-09-29 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0010_auto_20200928_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='column',
            unique_together={('id', 'order')},
        ),
    ]
