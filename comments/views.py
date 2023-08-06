from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from base.models import Problem, Category, Solution, SolutionVote, Comment, CommentVote
from base.models import UserToProblem
from comments.utils import update_comment_upvote_counter
from notifications.utils import notify_new_comment
from notifications.views import show_notifications
from .forms import CommentForm
import json

# Create your views here.
@login_required(login_url='account:login')
def create_comment(request):
    if request.method == 'POST':
        comment_content = request.POST.get('the_comment')
        solution_id = request.POST.get('solution_id')
        response_data = {}

        solution = get_object_or_404(Solution, pk=solution_id)
        comment = Comment(user=request.user, solution=solution, content=comment_content)
        comment.save()

        response_data['result'] = 'Create comment successful!'
        response_data['comment_id'] = comment.id
        response_data['comment_content'] = comment.content

        if request.user != comment.solution.user:
            notify_new_comment(comment)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        raise PermissionDenied()

@login_required(login_url='account:login')
def comment_vote_page(request, pk, vote):
    comment = get_object_or_404(Comment, pk=pk)
    if vote == 'upvote':
        if request.user != comment.user:
            vote, _ = CommentVote.objects.get_or_create(comment=comment, user=request.user)
            if vote.value == 1:
                vote.value = 0
            else:
                vote.value = 1
            vote.save()
            update_comment_upvote_counter(comment)

    elif vote == 'downvote':
        if request.user != comment.user:
            vote, _ = CommentVote.objects.get_or_create(comment=comment, user=request.user)
            if vote.value == -1:
                vote.value = 0
            else:
                vote.value = -1
            vote.save()
            update_comment_upvote_counter(comment)

    return HttpResponseRedirect(reverse('solutions:solutions', kwargs={'pk': comment.solution.problem.id}))




@login_required(login_url='account:login')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.user != request.user:
        raise PermissionDenied()
    comment.delete()
    return redirect('solutions:solutions', pk=comment.solution.problem.id)
