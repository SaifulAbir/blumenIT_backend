# Generated by Django 4.0 on 2023-02-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_homesinglerowdata_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homesinglerowdata',
            name='address',
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='shop_address',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
