# Generated by Django 4.0 on 2023-02-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_corporatedeal_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='homesinglerowdata',
            name='address',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
