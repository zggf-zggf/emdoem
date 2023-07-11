from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUser
from django.contrib.auth import get_user_model

# Create your views here.


def login_page(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(username=username)
        except:
            messages.error(request, 'Nie ma takiego użytkownika.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.error(request, 'Nazwa użytkownika lub hasło się nie zgadza.')

    context = {'page': page}
    return render(request, 'account/login_register.html', context)


def register_page(request):
    page = 'register'
    form = CreateUser()

    if request.method == 'POST':
        form = CreateUser(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home:home')
        else:
            messages.error(request, 'Wystąpił błąd podczas rejestracji.')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'account/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home:home')
