from django.db.models import Q
from django.shortcuts import render, redirect
from base.models import Problem, Category, Solution, SolutionVote, Comment, CommentVote
from .forms import UploadForm, SolutionForm, CommentForm
from base.models import UserToProblem
from django.shortcuts import get_object_or_404
from base.utils import get_watchers_of_problem, get_problem_stats, process_vote, update_solution_upvote_counter, update_comment_upvote_counter
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from notifications.utils import notify_new_comment
from notifications.views import show_notifications
from django.template.response import TemplateResponse
import json

@show_notifications
def problem_base(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    problems = Problem.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q)
    )
    categories = Category.objects.all()

    for problem in problems:
        stats = get_problem_stats(problem)
        setattr(problem, "watchers_count", stats["watching"])
        setattr(problem, "solved", stats["solved"])
        print(stats)

    context = {'problems': problems, 'categories': categories}
    return TemplateResponse(request, "problemBase/problemBase.html", context)


@show_notifications
@login_required(login_url='account:login')
def problem_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)
    utp.timestamp()

    solution_form = SolutionForm()

    if request.method == 'POST':
        solution_form = SolutionForm(request.POST)

        if solution_form.is_valid():
            solution = solution_form.save(commit=False)

            setattr(solution, 'user', request.user)
            setattr(solution, 'problem', problem)

            solution.save()

            return redirect('problems:solutions', pk=problem.id)

    context = {
        'name': problem.name,
        'problem_statement': problem.problem_statement,
        'pk': pk,
        'solution_form': solution_form
    }

    return TemplateResponse(request, "problemBase/problemStatement.html", context)


@show_notifications
@login_required
def problem_page_info(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    context = {
        'name': problem.name,
        'pk': pk,
        'problem_statement': problem.problem_statement,
        'added_by': problem.added_by,
        'creation_date': problem.creation_date,
        'category': problem.category,
    }

    return TemplateResponse(request, "problemBase/problemInfo.html", context);


@show_notifications
@login_required(login_url='account:login')
def upload_problem_page(request):
    upload_form = UploadForm()

    if request.method == 'POST':
        upload_form = UploadForm(request.POST)

        if upload_form.is_valid():
            created_problem = upload_form.save(commit=False)

            setattr(created_problem, "added_by", request.user)
            setattr(created_problem, "watchers", {created_problem.name: 1})
            setattr(created_problem, "solved", {created_problem.name: 0})

            created_problem.save()

            # Tutaj dodajemy userToProblem, automatycznie obserwujemy dodany problem.
            utp = UserToProblem()
            setattr(utp, 'user', request.user)
            setattr(utp, 'problem', created_problem)
            setattr(utp, 'is_watching', True)
            utp.save()

            return redirect('problems:problem_base')

    context = {'upload_form': upload_form}

    return TemplateResponse(request, "problemBase/problemUpload.html", context)


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

    context = {
        'name': problem.name,
        'pk': pk,
        'problem_statement': problem.problem_statement,
        'solutions': solutions,
        'comment_form': comment_form,
    }

    return TemplateResponse(request, "problemBase/problemSolution.html", context)

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

    return HttpResponseRedirect(reverse('problems:solutions', kwargs={'pk': solution.problem.id}))


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

    return HttpResponseRedirect(reverse('problems:solutions', kwargs={'pk': comment.solution.problem.id}))


@show_notifications
@login_required(login_url='account:login')
def solution_edit_page(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    problem = solution.problem

    if request.user != solution.user:
        return redirect('problems:solutions', pk=problem.id)

    solution_form = SolutionForm(request.POST or None, instance=solution)

    if solution_form.is_valid():
        solution = solution_form.save(commit=False)

        solution.save()
        return redirect('problems:solutions', pk=problem.id)

    context = {
        'solution_form': solution_form,
        'name': problem.name,
        'solution_id': pk,
        'pk': problem.id,
        'problem_statement': problem.problem_statement,
    }

    return TemplateResponse(request, "problemBase/solutionEdit.html", context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.user != request.user:
        raise PermissionDenied()
    comment.delete()
    return redirect('problems:solutions', pk=comment.solution.problem.id)
