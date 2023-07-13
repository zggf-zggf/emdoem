from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CreateUser
from base.utils import get_user_stats, get_problem_stats

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


def profile_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    problems_solved = user_stats.get('problems_solved')
    problems_added = user_stats.get('problems_added').order_by('-creation_date')
    solutions_added = user_stats.get('solutions_added').order_by('-creation_date')
    comments_added = user_stats.get('comments_added').order_by('-creation_date')

    context = {
        'user': user,
        'problems_solved_count': problems_solved.count,
        'problems_added': problems_added,
        'problems_added_count': problems_added.count(),
        'solutions_added': solutions_added,
        'solutions_added_count': solutions_added.count(),
        'comments_added': comments_added,
        'comments_added_count': comments_added.count(),
    }

    return render(request, 'account/user_overview.html', context)


def user_problems_added_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    problems_added = user_stats.get('problems_added').order_by('-creation_date')

    watching_stats = {}
    solved_stats = {}

    for problem in problems_added:
        problem_stats = get_problem_stats(problem)
        watching_stats[problem.id] = problem_stats['watching']
        solved_stats[problem.id] = problem_stats['solved']


    context = {
        'user': user,
        'problems_added': problems_added,
        'watching_stats': watching_stats,
        'solved_stats': solved_stats,
    }
    return render(request, 'account/user_problems_added.html', context)


def user_solutions_added_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    solutions_added = user_stats.get('solutions_added').order_by('-creation_date')

    context = {
        'user': user,
        'solutions_added': solutions_added,
    }

    return render(request, 'account/user_solutions_added.html', context)


def user_comments_added_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    comments_added = user_stats.get('comments_added').order_by('-creation_date')

    context = {
        'user': user,
        'comments_added': comments_added,
    }

    return render(request, 'account/user_comments_added.html', context)
