# Generated by Django 4.0 on 2022-09-21 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0093_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttags',
            name='title',
        ),
    ]