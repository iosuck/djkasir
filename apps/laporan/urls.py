from django.urls import path
from .views import LaporanListView, GeneratePDF
# GeneratePDF, LaporanDesignView

app_name = 'laporan'
urlpatterns = [
    path('', LaporanListView.as_view(), name='index'),
    path('invoice', GeneratePDF.as_view(), name='invoice'),
    # path('design', LaporanDesignView.as_view(), name='design'),
]
