# Generated by Django 4.0 on 2022-10-20 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0027_seller_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/logo'),
        ),
    ]