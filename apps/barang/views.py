from django.shortcuts import render
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.crypto import get_random_string
import datetime
from .models import Barang
from apps.cart.models import Cart


class BarangListTable(LoginRequiredMixin, BaseDatatableView):
    # The model we're going to show
    model = Barang

    # define the columns that will be returned
    columns = ['nama', 'harga', 'diskon', 'stok', 'id']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    # order_columns = ['number', 'user', 'state', '', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     if column == 'user':
    #         # escape HTML for security reasons
    #         return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
    #     else:
    #         return super(OrderListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(nama__icontains=search) |
                           Q(harga__icontains=search)
                           )
        return qs


class BarangIndexView(LoginRequiredMixin, TemplateView):
    template_name = "barang/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["resi"] = datetime.datetime.now().strftime(
            '%y%m%d') + "-" + str(cart_obj.id) + "-" + get_random_string(6).lower()
        return context
