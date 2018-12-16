from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.barang.models import Barang
from django.template.loader import get_template
from .models import Cart, CartItem
import datetime


class CartHomeView(LoginRequiredMixin, TemplateView):
    template_name = "cart/index.html"

    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        barang_id = request.POST['barang_id']
        qty = request.POST['qty']
        resi = request.POST.get('resi', None)
        barang_obj = Barang.objects.get(id=barang_id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        # buat resi baru
        if cart_obj.resi is None and resi is not None:
            cart_obj.resi = resi
            cart_obj.save()
            cart_item = CartItem.objects.create(cart=cart_obj, barang=barang_obj, qty=qty)
            messages.success(request, 'Di Tambahkan')
            return redirect('cart:index')
        # update barang
        if cart_obj.cartitem_set.all() is not None:
            cc = cart_obj.cartitem_set.all()
            update_barang = cc.filter(barang=barang_obj)
            if update_barang.count() == 1:
                simpan = update_barang.first()
                simpan.qty = qty
                simpan.save()
                messages.success(request, 'Update {simpan}'.format(simpan=simpan.barang))
                return redirect('cart:index')
        # buat pertama kali resi None dan item
        cart_item = CartItem.objects.create(cart=cart_obj, barang=barang_obj, qty=qty)
        messages.success(request, 'Di Tambahkan')
        return redirect('cart:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        if cart_obj.resi is not None:
            context['resi'] = cart_obj.resi
        context["cart"] = cart_obj
        return context


@login_required
def add_cart(request):
    ids = 1
    barang_obj = Barang.objects.get(id=ids)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_item = CartItem.objects.create(cart=cart_obj, barang=barang_obj)
    return HttpResponse('Berhasil')


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart/detail.html"

    def post(self, request, *args, **kwarg):
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cartitem = CartItem.objects.get(id=request.POST['cart_id'])
        cartitem.delete()
        return redirect(cart_obj.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        total = 0
        for x in cart_obj.cartitem_set.all():
            total += x.subtotal
        context["total"] = total
        return context

    def get_queryset(self):
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        return super().get_queryset()


@login_required
def CartBayar(request):
    if request.POST:
        kembali = request.POST['kembali2']
        bayar = request.POST['bayar']
        total = request.POST['total']
        # print(bayar)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_obj.total = int(total)
        cart_obj.bayar = int(bayar)
        cart_obj.kembali = int(kembali)
        cart_obj.save()
        item = 0
        for x in cart_obj.cartitem_set.all():
            item += x.qty
        context = {
            'laporan': cart_obj,
            'item': item,
        }
        return redirect('laporan:invoice')
        # return render(request, 'laporan/invoice.html', context)
        # del request.session['cart_id']
        # return redirect('laporan:index')
