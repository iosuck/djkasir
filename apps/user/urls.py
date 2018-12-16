from django.urls import path
from .views import loginPage, LogoutView

app_name = 'user'
urlpatterns = [
    path('', loginPage, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
