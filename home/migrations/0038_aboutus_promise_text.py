# Generated by Django 4.0 on 2023-05-21 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_remove_aboutus_content_aboutus_customer_relationship_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='promise_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]