# Generated by Django 4.0 on 2022-12-22 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0018_order_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PICKED', 'Picked'), ('DELIVERED', 'Delivered'), ('DELIVERED', 'Delivered'), ('RETURN', 'Return'), ('CANCEL', 'Cancel')], default='PENDING', max_length=20),
        ),
    ]