# Generated by Django 4.0 on 2023-04-06 10:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='full_description',
            field=ckeditor.fields.RichTextField(blank=True, default='', null=True),
        ),
    ]
