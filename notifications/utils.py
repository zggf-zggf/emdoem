from base.models import Comment, Solution
from notifications.models import NewCommentNotification, Notification, NewSolutionNotification
from base.utils import get_watchers_of_problem


def notify_new_comment(comment):
   notification = NewCommentNotification( type="comment",
                                         comment=comment,
                                         user=comment.solution.user,
                                         name=("@"+comment.user.username+" skomentował twoje rozwiązanie..."),
                                         content=("Użytkownik @"+comment.user.username+" dodał komentarz do twojego rozwiązania w zadaniu \""+comment.solution.problem.name+"\""))
   notification.save()


def notify_new_solution(solution):
    watchers = get_watchers_of_problem(solution.problem)
    print(watchers)
    for watcher in watchers:
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
        elif notification.type ==  "solution":
            setattr(notification, 'url', notification.newsolutionnotification.get_url())


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

