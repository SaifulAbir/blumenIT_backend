# Generated by Django 4.0 on 2022-01-06 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
                'db_table': 'tags',
            },
        ),
    ]