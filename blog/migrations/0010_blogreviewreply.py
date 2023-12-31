# Generated by Django 4.0 on 2023-05-10 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_is_vendor_user_is_seller'),
        ('blog', '0009_alter_blog_full_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogReviewReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('review_text', models.TextField(blank=True, default='', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_review_reply_review', to='blog.blogreview')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_review_reply_user', to='user.user')),
            ],
            options={
                'verbose_name': 'BlogReviewReply',
                'verbose_name_plural': 'BlogReviewReplies',
                'db_table': 'blog_review_reply',
            },
        ),
    ]
