# Generated by Django 5.0.6 on 2024-07-08 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='codigo_tic',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Código Tic'),
        ),
    ]
