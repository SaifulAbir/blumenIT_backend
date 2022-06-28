# Generated by Django 4.0 on 2022-06-28 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0012_alter_vendorrequest_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store_name', models.CharField(max_length=254, verbose_name='Organization/ Vendor Name')),
                ('address', models.CharField(blank=True, max_length=254, null=True, verbose_name='Address')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('logo', models.ImageField(upload_to='images/store_logo')),
                ('banner', models.ImageField(upload_to='images/banner')),
                ('phone', models.CharField(blank=True, default='None', max_length=255, null=True)),
                ('facebook', models.URLField()),
                ('twitter', models.URLField()),
                ('instagram', models.URLField()),
                ('youtube', models.URLField()),
                ('linkedin', models.URLField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vendor_settings', to='vendor.vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Store Setting',
                'verbose_name_plural': 'Store Settings',
                'db_table': 'store_settings',
            },
        ),
    ]
