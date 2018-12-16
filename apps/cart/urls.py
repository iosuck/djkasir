from django.urls import path
from .views import CartHomeView, CartDetailView, CartBayar

app_name = 'cart'
urlpatterns = [
    path('', CartHomeView.as_view(), name='index'),
    path('detail/<pk>', CartDetailView.as_view(), name='detail'),
    path('bayar/', CartBayar, name='bayar'),
]
