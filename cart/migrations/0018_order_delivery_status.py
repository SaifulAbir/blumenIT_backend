# Generated by Django 4.0 on 2022-12-22 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_alter_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PICKED', 'Picked'), ('DELIVERED', 'Delivered'), ('DELIVERED', 'Delivered'), ('RETURN', 'Return'), ('CANCEL', 'Cancel')], default='Picked', max_length=20),
        ),
    ]
