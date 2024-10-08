# Generated by Django 5.0.6 on 2024-06-10 19:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='titulo')),
                ('asunto', models.TextField(max_length=100, verbose_name='asunto')),
                ('proyecto', models.TextField(max_length=200, verbose_name='proyecto')),
                ('departamento', models.TextField(max_length=200, verbose_name='departamento')),
                ('estado', models.CharField(max_length=200, verbose_name='estado')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
