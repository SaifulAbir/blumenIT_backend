# Generated by Django 4.0 on 2022-10-25 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0028_alter_seller_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]