from django.shortcuts import render, redirect
from base.models import User


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        password = request.GET.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            print('error')

    context = {}
    return render(request, 'account/login_register.html', context)
