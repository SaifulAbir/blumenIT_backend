# Generated by Django 4.0 on 2023-05-16 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_mediachunk_mediafiles_chunk'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='image_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
