from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import User


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Nie ma takiego użytkownika.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.error(request, 'Nazwa użytkownika lub hasło się nie zgadza.')

    context = {}
    return render(request, 'account/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home:home')
