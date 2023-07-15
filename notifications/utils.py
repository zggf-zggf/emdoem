from base.models import Comment, Solution
from notifications.models import NewCommentNotification, Notification

def notify_new_comment(comment):
   notification = NewCommentNotification(comment=comment,
                                         user=comment.solution.user,
                                         name=("@"+comment.user.username+" skomentował twoje rozwiązanie..."),
                                         content=("@"+comment.user.username+" dodał komentarz do twojego rozwiązania w zadaniu \""+comment.solution.problem.name+"\""))
   notification.save()

def prepare_notifications(user):
    if user.is_authenticated:
        count = Notification.objects.filter(user=user, is_read=False).count()
        notifications = Notification.objects.filter(user=user).order_by('creation_date')[0 : 3]
        return {'count': count, 'notifications': notifications}

def prepare_all_notifications(user):
    if user.is_authenticated:
        notifications = Notification.objects.filter(user=user).order_by('creation_date')
        return {'notifications': notifications}

