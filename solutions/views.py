import json
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView

from base.models import Problem, Category, Solution, SolutionVote, Comment, CommentVote
from base.models import UserToProblem
from comments.forms import CommentForm
from notifications.utils import notify_new_comment, notify_new_solution, notify_new_problem
from notifications.views import show_notifications
from problembase.utils import has_user_solved_problem, get_problem_stats, add_stats_to_problems, add_status_to_problems, \
    get_watchers_of_problem
from problemset.utils import get_basic_problemset_data_for_problem
from ranking.utils import notify_problem_solved
from solutions.utils import update_solution_upvote_counter
from .forms import EditSolutionForm, SolutionForm
from .models import SolutionHistory


# Create your views here.
@show_notifications
@login_required(login_url='account:login')
def problem_solution_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    solutions = Solution.objects.filter(problem=problem).order_by('-upvote_counter')

    comment_form = CommentForm()

    for solution in solutions:
        setattr(solution, 'upvoted', SolutionVote.objects.filter(user=request.user, solution=solution, value=1).exists())
        setattr(solution, 'downvoted', SolutionVote.objects.filter(user=request.user, solution=solution, value=-1).exists())
        setattr(solution, 'comments', Comment.objects.filter(solution=solution).order_by('creation_date'))
        for comment in solution.comments:
            setattr(comment, 'upvoted', CommentVote.objects.filter(user=request.user, comment=comment, value=1).exists())
            setattr(comment, 'downvoted', CommentVote.objects.filter(user=request.user, comment=comment, value=-1).exists())

    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)

    waiting_for_surrender = (utp.began_surrendering and not utp.surrendered)
    if waiting_for_surrender:
        check_surrender_countdown(utp)

    display_solutions = has_user_solved_problem(request.user, problem) or utp.surrendered

    context = {
        'name': problem.name,
        'pk': pk,
        'problem_statement': problem.problem_statement,
        'solutions': solutions,
        'comment_form': comment_form,
        'display_solutions': display_solutions,
        'waiting_for_surrender': waiting_for_surrender,
        'problemset_data': get_basic_problemset_data_for_problem(problem, request.user),
    }

    return TemplateResponse(request, "solutions/problemSolution.html", context)

def check_surrender_countdown(utp):
    if utp.start_surrendering:
        end_time = utp.surrender_end_time
        if end_time < timezone.now():
            setattr(utp, 'surrendered', True)
            utp.save()

@login_required(login_url='account:login')
def solution_vote_page(request, pk, vote):
    solution = get_object_or_404(Solution, pk=pk)
    if vote == 'upvote':
        if request.user != solution.user:
            vote, _ = SolutionVote.objects.get_or_create(solution=solution, user=request.user)
            if vote.value == 1:
                vote.value = 0
            else:
                vote.value = 1
            vote.save()
            update_solution_upvote_counter(solution)

    elif vote == 'downvote':
        if request.user != solution.user:
            vote, _ = SolutionVote.objects.get_or_create(solution=solution, user=request.user)
            if vote.value == -1:
                vote.value = 0
            else:
                vote.value = -1
            vote.save()
            update_solution_upvote_counter(solution)

    return HttpResponseRedirect(reverse('solutions:solutions', kwargs={'pk': solution.problem.id}))

@show_notifications
@login_required(login_url='account:login')
def solution_edit_page(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    problem = solution.problem

    if request.user != solution.user:
        return redirect('solutions:solutions', pk=problem.id)

    solution_form = EditSolutionForm(request.POST or None, instance=solution)

    if solution_form.is_valid():
        solution = solution_form.save(commit=False)

        solution.save()
        return redirect('solutions:solutions', pk=problem.id)

    context = {
        'solution_form': solution_form,
        'name': problem.name,
        'solution_id': pk,
        'pk': problem.id,
        'problem_statement': problem.problem_statement,
    }

    return TemplateResponse(request, "solutions/solutionEdit.html", context)

@login_required(login_url='account:login')
def begin_surrender_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(user=request.user, problem=problem)

    utp.start_surrendering()

    response_data = {}
    response_data['result'] = 'success!'
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required(login_url='account:login')
def get_surrender_time(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(user=request.user, problem=problem)

    end_time = utp.surrender_end_time
    # Calculate the remaining time (time left until end_time)
    remaining_time = end_time - timezone.now()

    # Extract minutes and seconds from the remaining time
    minutes = remaining_time.seconds // 60
    seconds = remaining_time.seconds % 60

    response_data = {}
    response_data['result'] = 'success'
    response_data['remaining_minutes'] = minutes
    response_data['remaining_seconds'] = seconds

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required(login_url='account:login')
def revert_surrender_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)

    if not utp.surrendered:
        utp.began_surrendering = False
        utp.surrender_end_time = None
        utp.save()

    return redirect('solutions:solutions', pk=problem.id)

@login_required(login_url='account:login')
def solution_history_page(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    problem = solution.problem
    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)

    if not (has_user_solved_problem(request.user, problem) or utp.surrendered):
        raise PermissionDenied()

    history_list = SolutionHistory.objects.filter(solution=solution).order_by('-date')
    context = {
        'problem_name': problem.name,
        'pk': pk,
        'history_list': history_list,
    }

    return render(request, "solutions/_solutionHistory.html", context)

