from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from apps.cart.models import Cart
from projectkerja.utils import render_to_pdf
from django.template.loader import get_template
from django.http import HttpResponse
from apps.cart.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime


class LaporanListView(LoginRequiredMixin, ListView):
    ordering = ('-created_at')
    template_name = "laporan/index.html"

    def get_queryset(self):
        qs = Cart.objects.filter(user=self.request.user)
        return qs

# class LaporanDesignView(TemplateView):
#     template_name = "laporan/invoice.html"


class GeneratePDF(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        item = 0
        for x in cart_obj.cartitem_set.all():
            item += x.qty
        context = {
            'laporan': cart_obj,
            'item': item,
        }
        pdf = render_to_pdf('laporan/invoice.html', context)
        del request.session['cart_id']
        return HttpResponse(pdf, content_type='application/pdf')
        # template = get_template('laporan/invoice.html')
        # context = {
        #     "invoice_id": 123,
        #     "customer_name": "John Cooper",
        #     "amount": 1399.99,
        #     "today": "Today",
        # }
        # html = template.render(context)
        # pdf = render_to_pdf('laporan/invoice.html', context)
        # if pdf:
        #     response = HttpResponse(pdf, content_type='application/pdf')
        #     filename = "Invoice_%s.pdf" % ("12341231")
        #     content = "inline; filename='%s'" % (filename)
        #     download = request.GET.get("download")
        #     if download:
        #         content = "attachment; filename='%s'" % (filename)
        #     response['Content-Disposition'] = content
        #     return response
        # return HttpResponse("Not found")
