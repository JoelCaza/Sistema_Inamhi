# Generated by Django 5.0.6 on 2024-06-10 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='proyecto',
        ),
        migrations.AddField(
            model_name='ticket',
            name='descripcion',
            field=models.CharField(default='Valor predeterminado', max_length=100),
        ),
    ]
