from django.db import models


class Barang(models.Model):
    nama = models.CharField("Nama Barang", max_length=200)
    harga = models.IntegerField("Harga")
    stok = models.IntegerField("Stok", blank=True, null=True)
    diskon = models.IntegerField("Diskon", blank=True, null=True)

    def __str__(self):
        return self.nama
