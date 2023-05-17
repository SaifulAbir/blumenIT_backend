# Generated by Django 4.0 on 2023-05-17 08:49

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0080_productreviewreply'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='products', validators=[product.models.CategoryImages.validate_file_extension])),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category_image_category', to='product.category')),
            ],
            options={
                'verbose_name': 'CategoryImage',
                'verbose_name_plural': 'CategoryImages',
                'db_table': 'category_images',
            },
        ),
    ]
