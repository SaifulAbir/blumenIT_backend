# Generated by Django 4.0 on 2022-10-25 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0118_alter_product_in_house_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(default='', help_text='name', max_length=100, unique=True),
        ),
    ]