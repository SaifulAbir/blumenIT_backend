# Generated by Django 4.0 on 2022-11-15 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0159_specificationtitle_alter_specification_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_gaming',
        ),
    ]
