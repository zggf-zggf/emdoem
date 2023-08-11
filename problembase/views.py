import json
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.http import JsonResponse

from base.models import Problem, Category, Solution, SolutionVote, Comment, CommentVote
from base.models import UserToProblem
from comments.utils import update_comment_upvote_counter
from notifications.utils import notify_new_comment, notify_new_solution, notify_new_problem
from notifications.views import show_notifications
from problembase.utils import has_user_solved_problem, get_problem_stats, add_stats_to_problems, add_status_to_problems, \
    get_watchers_of_problem
from ranking.utils import notify_problem_solved
from solutions.forms import SolutionForm
from solutions.utils import update_solution_upvote_counter
from .forms import UploadForm, EditProblemForm
from .models import ProblemHistory
from problemset.models import Problemset
from problemset.utils import problem_in_problemset_preview, get_basic_problemset_data_for_problem


@method_decorator(show_notifications, name='dispatch')
class ProblemBaseView(ListView):
    model = Problem
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        object_list = Problem.objects.filter(
            Q(category__name__icontains=q) |
            Q(name__icontains=q)
        ).order_by('-creation_date')
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

            return redirect('solutions:solutions', pk=problem.id)

    problem_stats = get_problem_stats(problem)

    context = {
        'name': problem.name,
        'problem_statement': problem.problem_statement,
        'pk': pk,
        'solution_form': solution_form,
        'watching_count': problem_stats['watching'],
        'watched': utp.is_watching,
        'added_by': problem.added_by,
        'edited': problem.edited,
        'surrendered': utp.surrendered,
        'sent_solution': Solution.objects.filter(problem=problem, user=request.user).exists(),
    }
    if utp.seen_in_problemset:
        context['problemset_data'] = problem_in_problemset_preview(problem, utp.seen_in_problemset, request.user)
        print(context['problemset_data'])

    return TemplateResponse(request, "problembase/problemStatement.html", context)


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
        'source': problem.source,
        'edited': problem.edited,
        'problemset_data': get_basic_problemset_data_for_problem(problem, request.user),
    }

    return TemplateResponse(request, "problembase/problemInfo.html", context);


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
            utp.timestamp()
            utp.save()

            notify_new_problem(created_problem)

            return redirect('problems:problem_base')

    context = {'upload_form': upload_form}

    return TemplateResponse(request, "problembase/problemUpload.html", context)


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


@show_notifications
@login_required(login_url='account:login')
def problem_edit_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    if request.user != problem.added_by:
        return redirect('problems:statement', pk=problem.id)

    problem_form = EditProblemForm(request.POST or None, instance=problem)
    if problem_form.is_valid():
        problem = problem_form.save(commit=False)

        problem.save()
        return redirect('problems:statement', pk=problem.id)

    context = {
        'problem_form': problem_form,
        'name': problem.name,
        'problem_id': pk,
        'pk': problem.id,
        'problem_statement': problem.problem_statement,
    }
    return TemplateResponse(request, "problembase/problemEdit.html", context)

def problem_history_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    history_list = ProblemHistory.objects.filter(problem=problem).order_by('-date')
    context = {
        'problem_name': problem.name,
        'pk': pk,
        'history_list': history_list,
    }

    return render(request, "problembase/_problemHistory.html", context)

@login_required(login_url='account:login')
def upload_problem_api(request):
    upload_form = UploadForm()

    if request.method == 'POST':
        upload_form = UploadForm(request.POST)
        response_data = {}
        if upload_form.is_valid():
            created_problem = upload_form.save(commit=False)

            setattr(created_problem, "added_by", request.user)
            created_problem.save()

            utp = UserToProblem()
            setattr(utp, 'user', request.user)
            setattr(utp, 'problem', created_problem)
            setattr(utp, 'is_watching', True)
            utp.timestamp()
            utp.save()

            response_data = {
                'result': 'Success',
                'problem_id': created_problem.id,
            }
        else:
            response_data = {
                'result': 'Form invalid',
            }
        return JsonResponse(response_data)
    else:
        raise PermissionDenied()

def problem_statement_api(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problembase/_problemStatementApi.html', {'statement': problem.problem_statement})