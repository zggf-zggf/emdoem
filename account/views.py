from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import User


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        password = request.GET.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            # Trzeba zrobić obsługę tego błędu.
            messages.error(request, 'Nie ma takiego użytkownika.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home:home')


    context = {}
    return render(request, 'account/login_register.html', context)
