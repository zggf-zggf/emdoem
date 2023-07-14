from base.models import Comment, Solution
from notifications.models import NewCommentNotification

def notify_new_comment(comment):
   notification = NewCommentNotification(comment=comment,
                                         user=comment.solution.user,
                                         name=("@"+comment.user.username+" skomentował twoje rozwiązanie..."),
                                         content=("@"+comment.user.username+" dodał komentarz do twojego rozwiązania w zadaniu \""+comment.solution.problem.name+"\""))
   notification.save()

def prepare_notifications(user):
    if user.is_authenticated:
        count = NewCommentNotification.objects.filter(user=user, is_read=False).count()
        notifications = NewCommentNotification.objects.filter(user=user, is_read=False).order_by('creation_date')[0 : 3]
        return {'count': count, 'notifications': notifications}

