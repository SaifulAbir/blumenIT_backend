# Generated by Django 4.0 on 2023-01-08 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0025_delete_orderitemcombination'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='warranty',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
