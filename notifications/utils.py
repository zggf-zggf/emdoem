from base.models import Comment, Solution
from notifications.models import NewCommentNotification, Notification

def notify_new_comment(comment):
   notification = NewCommentNotification(comment=comment,
                                         user=comment.solution.user,
                                         name=("@"+comment.user.username+" skomentował twoje rozwiązanie..."),
                                         content=("Użytkownik @"+comment.user.username+" dodał komentarz do twojego rozwiązania w zadaniu \""+comment.solution.problem.name+"\""))
   notification.save()

def attach_urls(notifications):
    for notification in notifications:
        match notification.type:
            case "comment":
                setattr(notification, 'url', notification.newcommentnotification.get_url)

def prepare_notifications(user):
    if user.is_authenticated:
        count = Notification.objects.filter(user=user, is_read=False).count()
        notifications = Notification.objects.filter(user=user).order_by('creation_date')[0 : 3]
        attach_urls(notifications)
        return {'count': count, 'notifications': notifications}

def prepare_all_notifications(user):
    if user.is_authenticated:
        notifications = Notification.objects.filter(user=user).order_by('creation_date')
        attach_urls(notifications)
        return {'notifications': notifications}

