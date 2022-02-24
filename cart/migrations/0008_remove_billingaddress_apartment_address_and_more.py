# Generated by Django 4.0 on 2022-02-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='apartment_address',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='company_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='email',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='street_address',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='zip_code',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]