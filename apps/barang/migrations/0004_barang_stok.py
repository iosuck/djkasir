# Generated by Django 2.1.3 on 2018-12-14 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barang', '0003_auto_20181214_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='barang',
            name='stok',
            field=models.IntegerField(blank=True, null=True, verbose_name='Stok'),
        ),
    ]