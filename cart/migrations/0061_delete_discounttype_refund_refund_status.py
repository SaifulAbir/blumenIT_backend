# Generated by Django 4.0 on 2022-10-23 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0060_discounttype_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DiscountType',
        ),
        migrations.AddField(
            model_name='refund',
            name='refund_status',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
