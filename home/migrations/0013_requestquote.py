# Generated by Django 4.0 on 2023-02-01 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_delete_dealsoftheday'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('company_name', models.CharField(blank=True, max_length=120)),
                ('website', models.CharField(blank=True, max_length=120)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('services', models.CharField(choices=[('Wholesale Business Plan', 'Wholesale'), ('Retail Business Plan', 'Retail'), ('Reseller Business Plan', 'Reseller'), ('Support Business Plan', 'Support'), ('Sales Business Plan', 'Sales'), ('Others', 'Others')], max_length=120)),
                ('overview', models.TextField()),
            ],
            options={
                'verbose_name': 'RequestQuote',
                'verbose_name_plural': 'RequestQuotes',
                'db_table': 'request_quote',
            },
        ),
    ]
