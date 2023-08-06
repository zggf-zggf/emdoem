from django.db.models import Sum
from base.models import CommentVote
def update_comment_upvote_counter(comment):
    comment.upvote_counter = CommentVote.objects.filter(comment=comment).aggregate(Sum('value'))['value__sum']
    comment.save()

