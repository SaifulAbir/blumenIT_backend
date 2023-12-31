# Generated by Django 4.0 on 2022-12-13 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_customerprofile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket_id', models.SlugField()),
                ('ticket_title', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='support_user', to='user.user')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'tickets',
                'db_table': 'ticket',
            },
        ),
    ]
