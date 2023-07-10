from django.shortcuts import render

# Create your views here.


def login(request):
    context = {}
    return render(request, 'account/login_register.html', context)
