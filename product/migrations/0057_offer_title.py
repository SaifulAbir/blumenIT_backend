# Generated by Django 4.0 on 2023-01-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0056_remove_offer_product_offerproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='title',
            field=models.CharField(default='', help_text='name', max_length=100),
        ),
    ]
