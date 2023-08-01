from base.models import Comment, Solution
from notifications.models import NewCommentNotification, Notification, NewSolutionNotification, NewProblemNotification
from base.utils import get_watchers_of_problem
from django.contrib.auth import get_user_model
from base.models import UserToProblem

def notify_new_comment(comment):
   notification = NewCommentNotification( type="comment",
                                         comment=comment,
                                         user=comment.solution.user,
                                         name=("@"+comment.user.username+" skomentował twoje rozwiązanie..."),
                                         content=("Użytkownik @"+comment.user.username+" dodał komentarz do twojego rozwiązania w zadaniu \""+comment.solution.problem.name+"\""))
   notification.save()

def notify_new_problem(problem):
    users = get_user_model().objects.all()
    for user in users:
        if user != problem.added_by:
            if not UserToProblem.objects.filter(problem=problem, user=user).exists():
                notification = NewProblemNotification( type="problem",
                                           problem=problem,
                                           user=user,
                                           name=("Nowe zadanie w kategorii " + problem.category.name + "."),
                                           content=("@"+problem.added_by.username+" dodał nowe zadanie które może cię zainteresować w kategorii " + problem.category.name))
                notification.save()

def notify_new_solution(solution):
    watchers = get_watchers_of_problem(solution.problem)
    print(watchers)
    for watcher in watchers:
        if solution.user != watcher:
            notification = NewSolutionNotification(type="solution",
                                              solution=solution,
                                              user_id=watcher['user'],
                                              name=("@"+solution.user.username+" dodał rozwiązanie"),
                                              content=("Użytkownik @"+solution.user.username+" dodał rozwiązanie do zadania \""+solution.problem.name+"\""))
            notification.save()


def attach_urls(notifications):
    for notification in notifications:
        if notification.type == "comment":
            setattr(notification, 'url', notification.newcommentnotification.get_url())
        elif notification.type == "solution":
            setattr(notification, 'url', notification.newsolutionnotification.get_url())
        elif notification.type == "problem":
            setattr(notification, 'url', notification.newproblemnotification.get_url())


    # for notification in notifications:
    #     match notification.type:
    #         case "comment":
    #             setattr(notification, 'url', notification.newcommentnotification.get_url())
    #         case "solution":
    #             setattr(notification, 'url', notification.newsolutionnotification.get_url())


def prepare_notifications(user):
    if user.is_authenticated:
        count = Notification.objects.filter(user=user, is_read=False).count()
        notifications = Notification.objects.filter(user=user).order_by('-creation_date')[0 : 3]
        attach_urls(notifications)
        return {'count': count, 'notifications': notifications}


def prepare_all_notifications(user):
    if user.is_authenticated:
        notifications = Notification.objects.filter(user=user).order_by('-creation_date')
        attach_urls(notifications)
        return {'notifications': notifications}

