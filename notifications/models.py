from django.db import models
from base.models import Comment, Solution, User
from django.urls import reverse

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        abstract = True

    def get_url(self):
        raise NotImplementedError('this method is abstract')

class NewCommentNotification(Notification):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('problems:solutions', kwargs={'pk': self.comment.solution.problem.id})

    url = property(get_url)
