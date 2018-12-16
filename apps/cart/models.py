from django.db import models
from apps.barang.models import Barang
from projectkerja import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = self.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.get_queryset().create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    resi = models.CharField("Resi", max_length=50, blank=True, null=True)
    total = models.IntegerField("Total", blank=True, null=True)
    bayar = models.IntegerField("Bayar", blank=True, null=True)
    kembali = models.IntegerField("Kembali", blank=True, null=True)
    created_at = models.DateTimeField("Created At", auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True, auto_now_add=False)

    objects = CartManager()

    def __str__(self):
        return "{id}".format(id=self.id)

    def get_absolute_url(self):
        return reverse("cart:detail", kwargs={"pk": self.pk})


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    subtotal = models.IntegerField("Subtotal", blank=True, null=True)
    qty = models.IntegerField("QTY", blank=True, null=True)
    objects = CartManager()

    def __str__(self):
        return "{id}".format(id=self.id)


def pre_save_cartitem(sender, instance, *args, **kwargs):
    total = 0
    total_diskon = 0
    harga = int(instance.barang.harga)
    qty = int(instance.qty)
    for x in range(0, qty):
        total += harga
    if instance.barang.diskon is not None:
        diskon = total/100*int(instance.barang.diskon)
        total_diskon = total-diskon
    else:
        total_diskon = total
    instance.subtotal = total_diskon


pre_save.connect(pre_save_cartitem, sender=CartItem)


def post_save_cartitem(sender, instance, created, *args, **kwargs):
    total = 0
    total_diskon = 0
    harga = int(instance.barang.harga)
    qty = int(instance.qty)
    for x in range(0, qty):
        total += harga
    if instance.barang.diskon is not None:
        diskon = total/100*int(instance.barang.diskon)
        total_diskon = total-diskon
    else:
        total_diskon = total
    instance.subtotal = total_diskon


post_save.connect(post_save_cartitem, sender=CartItem)
