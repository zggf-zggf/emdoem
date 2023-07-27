from django.shortcuts import render, redirect
from base.models import Problem, UserToProblem
from base.utils import add_stats_to_problems, add_status_to_problems
from notifications.utils import prepare_notifications
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return home_page(request)
    else:
        return welcome_page(request)

def welcome_page(request):
    return render(request, "home/index.html")

def home_page(request):
    utps = UserToProblem.objects.filter(user=request.user).order_by("last_visit")[:5]
    recently_visited = []
    for utp in utps:
        recently_visited.append(utp.problem)

    add_stats_to_problems(recently_visited)
    add_status_to_problems(recently_visited, request.user)
    notifications_data = prepare_notifications(request.user)
    context = {
        'recently_visited': recently_visited,
        'notifications_data': notifications_data,
    }
    return render(request, "home/home.html", context)
