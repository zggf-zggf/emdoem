from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CreateUser, LoginUserForm
from problembase.utils import get_user_stats, get_problem_stats, has_user_solved_problem
from notifications.views import show_notifications
from django.template.response import TemplateResponse
from itertools import chain
from operator import attrgetter
from django.core.exceptions import PermissionDenied
from notifications.utils import prepare_all_notifications
from ranking.utils import get_ranking
from base.models import Problem
from solutions.utils import can_see_solutions

# Create your views here.


def login_page(request):
    page = 'login'

    if request.method == 'POST':
        valuenext = request.GET.get('next')
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username'].lower()
            password = data['password']

            try:
                user = get_user_model().objects.get(username=username)
            except:
                messages.error(request, 'Nie ma takiego użytkownika.')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if valuenext is not None:
                    return redirect(valuenext)
                else:
                    return redirect('home:home')
            else:
                messages.error(request, 'Nazwa użytkownika lub hasło się nie zgadza.')

    form = LoginUserForm()
    context = {'page': page, 'form': form}
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


@show_notifications
def profile_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    problems_solved = user_stats.get('problems_solved')
    problems_added = user_stats.get('problems_added').order_by('-creation_date')
    solutions_added = user_stats.get('solutions_added').order_by('-creation_date')
    comments_added = user_stats.get('comments_added').order_by('-creation_date')

    for problem in problems_added:
        setattr(problem, 'solved', True)

    for comment in comments_added:
        setattr(comment, 'solved', True)

    for solution in solutions_added:
        if request.user.is_authenticated:
            setattr(solution, 'solved',
                    has_user_solved_problem(request.user, Problem.objects.get(id=solution.problem_id)))
        else:
            setattr(solution, 'solved', False)

    recent_activities = sorted(
        chain(problems_added, solutions_added, comments_added),
        key=attrgetter('creation_date'),
        reverse=True,
    )

    recent_activities = recent_activities[:4]

    ranking = get_ranking()

    context = {
        'user': user,
        'problems_solved_count': problems_solved.count,
        'problems_added': problems_added,
        'problems_added_count': problems_added.count(),
        'solutions_added': solutions_added,
        'solutions_added_count': solutions_added.count(),
        'comments_added': comments_added,
        'comments_added_count': comments_added.count(),
        'recent_activities': recent_activities,
        'users_ranking': ranking['users_ranking'],
        'user_position': ranking['user_position'],
    }

    return TemplateResponse(request, 'account/user_overview.html', context)


@show_notifications
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
    return TemplateResponse(request, 'account/user_problems_added.html', context)


@show_notifications
def user_solutions_added_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    solutions_added = user_stats.get('solutions_added').order_by('-creation_date')

    for solution in solutions_added:
        if request.user.is_authenticated:
            setattr(solution, 'visible', can_see_solutions(request.user, solution.problem))
        else:
            setattr(solution, 'visible', False)

    context = {
        'user': user,
        'solutions_added': solutions_added,
    }

    return TemplateResponse(request, 'account/user_solutions_added.html', context)


@show_notifications
def user_comments_added_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_stats = get_user_stats(user)

    comments_added = user_stats.get('comments_added').order_by('-creation_date')

    context = {
        'user': user,
        'comments_added': comments_added,
    }

    return TemplateResponse(request, 'account/user_comments_added.html', context)


@show_notifications
def user_notifications_page(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    if request.user != user:
        raise PermissionDenied()

    all_notifications_data = prepare_all_notifications(user)
    context = {
        'user': user,
        'all_notifications_data': all_notifications_data
    }

    return TemplateResponse(request, 'account/user_notifications.html', context)
