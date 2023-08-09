from django.shortcuts import render, redirect
from base.models import Problem, UserToProblem
from problembase.utils import add_stats_to_problems, add_status_to_problems
from notifications.utils import prepare_notifications
from .models import Announcement
from problemset.models import UserToProblemset
from problemset.utils import check_for_problemset_editing_notification, process_problemset_content, attach_problemset_progress
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return home_page(request)
    else:
        return welcome_page(request)


def welcome_page(request):
    return render(request, "home/index.html")


def home_page(request):
    utps = UserToProblem.objects.filter(user=request.user, last_visit__isnull=False).order_by("-last_visit")[:5]
    utpsets = UserToProblemset.objects.filter(user=request.user, last_visit__isnull=False).order_by("-last_visit")[:4]
    recently_visited = []
    for utp in utps:
        recently_visited.append(utp.problem)

    recently_visited_problemsets = []
    for utpset in utpsets:
        problemset = utpset.problemset
        process_problemset_content(problemset.content, request.user)
        attach_problemset_progress(problemset, request.user)
        recently_visited_problemsets.append(problemset)


    add_stats_to_problems(recently_visited)
    add_status_to_problems(recently_visited, request.user)
    notifications_data = prepare_notifications(request.user)
    announcements = Announcement.objects.filter(is_visible=True).order_by('-date')[:5]
    home_notifications = {
        'problemset_editing': check_for_problemset_editing_notification(request.user),
    }
    context = {
        'recently_visited': recently_visited,
        'recently_visited_problemsets': recently_visited_problemsets,
        'notifications_data': notifications_data,
        'announcements': announcements,
        'home_notifications': home_notifications,
    }
    return render(request, "home/home.html", context)
