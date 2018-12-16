# Generated by Django 2.1.3 on 2018-12-13 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('barang', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('bayar', models.IntegerField(verbose_name='Bayar')),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barang.Barang')),
            ],
        ),
    ]
