from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from projectkerja import settings
# Create your views here.
User = settings.AUTH_USER_MODEL


def loginPage(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cart:index')
    return render(request, 'user/login.html')


class LogoutView(LogoutView):
    next_page = "/"
