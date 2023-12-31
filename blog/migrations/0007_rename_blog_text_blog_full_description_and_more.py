# Generated by Django 4.0 on 2023-01-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='blog_text',
            new_name='full_description',
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog'),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_keywords',
            field=models.CharField(default='', help_text='name', max_length=100),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_title',
            field=models.CharField(default='', help_text='name', max_length=100),
        ),
        migrations.AddField(
            model_name='blog',
            name='short_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
