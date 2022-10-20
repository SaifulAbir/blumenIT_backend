# Generated by Django 4.0 on 2022-10-19 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_subscription'),
        ('vendor', '0024_alter_vendor_vendor_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.user'),
        ),
        migrations.AlterField(
            model_name='vendorrequest',
            name='is_verified',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
