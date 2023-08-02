from django.db.models import Q
from django.shortcuts import render, redirect
from base.models import Problem, Category, Solution, SolutionVote, Comment, CommentVote
from .forms import UploadForm, SolutionForm, CommentForm
from base.models import UserToProblem
from django.shortcuts import get_object_or_404
from base.utils import get_watchers_of_problem, get_problem_stats, process_vote, update_solution_upvote_counter, update_comment_upvote_counter, solved_problem, add_stats_to_problems, add_status_to_problems
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from notifications.utils import notify_new_comment, notify_new_solution, notify_new_problem
from notifications.views import show_notifications
from django.template.response import TemplateResponse
import json
from django.utils import timezone
from datetime import timedelta
from ranking.utils import notify_problem_solved
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


#legacy code
@show_notifications
def problem_base(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    problems = Problem.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q)
    )
    categories = Category.objects.all()

    add_stats_to_problems(problems)
    add_status_to_problems(problems, request.user)

    context = {'problems': problems, 'categories': categories}
    return TemplateResponse(request, "problemBase/problemBase.html", context)


@method_decorator(show_notifications, name='dispatch')
class ProblemBaseView(ListView):
    model = Problem
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        object_list = Problem.objects.filter(
            Q(category__name__icontains=q) |
            Q(name__icontains=q)
        )
        return object_list
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        add_stats_to_problems(data['object_list'])
        add_status_to_problems(data['object_list'], self.request.user)
        return data








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
            notify_new_solution(solution)
            notify_problem_solved(problem, request.user)

            return redirect('problems:solutions', pk=problem.id)

    problem_stats = get_problem_stats(problem)

    context = {
        'name': problem.name,
        'problem_statement': problem.problem_statement,
        'pk': pk,
        'solution_form': solution_form,
        'watching_count': problem_stats['watching'],
        'watched': utp.is_watching,
    }

    return TemplateResponse(request, "problemBase/problemStatement.html", context)


@show_notifications
@login_required(login_url='account:login')
def problem_page_info(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    context = {
        'name': problem.name,
        'pk': pk,
        'problem_statement': problem.problem_statement,
        'added_by': problem.added_by,
        'creation_date': problem.creation_date,
        'category': problem.category,
        'source': problem.source
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

            notify_new_problem(created_problem)

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

    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)

    waiting_for_surrender = (utp.began_surrendering and not utp.surrendered)
    if waiting_for_surrender:
        check_surrender_countdown(utp)

    display_solutions = solved_problem(request.user, problem) or utp.surrendered

    context = {
        'name': problem.name,
        'pk': pk,
        'problem_statement': problem.problem_statement,
        'solutions': solutions,
        'comment_form': comment_form,
        'display_solutions': display_solutions,
        'waiting_for_surrender': waiting_for_surrender,
    }

    return TemplateResponse(request, "problemBase/problemSolution.html", context)


def check_surrender_countdown(utp):
    if utp.start_surrendering:
        end_time = utp.surrender_end_time
        if end_time < timezone.now():
            setattr(utp, 'surrendered', True)
            utp.save()


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
def watch_problem_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)

    if utp.is_watching:
        setattr(utp, 'is_watching', False)
    else:
        setattr(utp, 'is_watching', True)

    utp.save()

    return HttpResponseRedirect(reverse('problems:statement', kwargs={'pk': pk}))


@login_required(login_url='account:login')
def problem_surrender_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)

    setattr(utp, 'surrendered', True)
    utp.save()

    return HttpResponseRedirect(reverse('problems:solutions', kwargs={'pk': problem.id}))


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


@login_required(login_url='account:login')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.user != request.user:
        raise PermissionDenied()
    comment.delete()
    return redirect('problems:solutions', pk=comment.solution.problem.id)


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

    return redirect('problems:solutions', pk=problem.id)
