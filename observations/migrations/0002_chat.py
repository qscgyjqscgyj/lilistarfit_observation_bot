# Generated by Django 4.2.13 on 2024-05-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=255, unique=True, verbose_name='ID чата')),
                ('last_messages', models.JSONField(verbose_name='Последние сообщения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'ordering': ['chat_id'],
            },
        ),
    ]