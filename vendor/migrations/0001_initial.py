# Generated by Django 4.0 on 2022-01-06 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VendorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('organization_name', models.CharField(max_length=254, unique=True, verbose_name='Organization/ Vendor Name')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('vendor_status', models.CharField(choices=[('ORGANIZATION', 'Organization'), ('INDIVIDUAL', 'Individual')], max_length=20)),
                ('nid', models.CharField(max_length=50)),
                ('trade_license', models.ImageField(blank=True, null=True, upload_to='images/trade_license')),
            ],
            options={
                'verbose_name': 'Vendor Request',
                'verbose_name_plural': 'Vendor Requests',
                'db_table': 'vendor_requests',
            },
        ),
    ]
