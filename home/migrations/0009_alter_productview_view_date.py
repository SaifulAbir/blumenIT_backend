# Generated by Django 4.0 on 2022-02-23 05:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_productview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productview',
            name='view_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]