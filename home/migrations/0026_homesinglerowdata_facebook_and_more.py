# Generated by Django 4.0 on 2023-04-04 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_alter_advertisement_work_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='homesinglerowdata',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='footer_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='footer_logo',
            field=models.ImageField(blank=True, null=True, upload_to='HomeImage'),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='header_logo',
            field=models.ImageField(blank=True, null=True, upload_to='HomeImage'),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='messenger',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='whatsapp',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homesinglerowdata',
            name='youtube',
            field=models.URLField(blank=True, null=True),
        ),
    ]