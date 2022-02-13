# Generated by Django 4.0 on 2022-02-13 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_paymenttype_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(allow_unicode=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'ShippingType',
                'verbose_name_plural': 'ShippingTypes',
                'db_table': 'shipping_types',
            },
        ),
    ]
