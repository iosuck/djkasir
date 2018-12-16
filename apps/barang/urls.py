from django.urls import path
from .views import BarangListTable, BarangIndexView

app_name = 'barang'
urlpatterns = [
    path('', BarangIndexView.as_view(), name='index'),
    path('barang-list', BarangListTable.as_view(), name='barang_list'),
]
