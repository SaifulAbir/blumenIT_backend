# Generated by Django 4.0 on 2023-04-06 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_is_vendor_user_is_seller'),
        ('vendor', '0006_seller_password_seller_seller_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='seller_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='seller_seller_user', to='user.user'),
        ),
    ]
