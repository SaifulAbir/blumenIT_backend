# Generated by Django 4.0 on 2022-02-08 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_paymenttype_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymenttype',
            old_name='notes',
            new_name='note',
        ),
    ]
