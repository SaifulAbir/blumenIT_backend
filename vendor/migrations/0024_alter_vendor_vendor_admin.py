# Generated by Django 4.0 on 2022-10-19 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_subscription'),
        ('vendor', '0023_alter_vendor_email_alter_vendor_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_admin', to='user.user', verbose_name='Vendor Admin'),
        ),
    ]
