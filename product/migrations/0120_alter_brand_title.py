# Generated by Django 4.0 on 2022-10-25 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0119_alter_brand_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]