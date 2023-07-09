from django.http import Http404
from django.shortcuts import render, redirect
from base.models import Problem
from .forms import UploadForm, SolutionForm
from base.models import UserToProblem
from django.shortcuts import get_object_or_404
from base.utils import get_watchers_of_problem, get_problem_stats
from django.contrib.auth.decorators import login_required


def problem_base(request):
    problems = Problem.objects.all()
    for problem in problems:
        stats = get_problem_stats(problem)
        setattr(problem, "watchers_count", stats["watching"])
        setattr(problem, "solved", stats["solved"])
        print(stats)

    context = {'problems': problems}
    return render(request, "problemBase/problemBase.html", context)


@login_required
def problem_page(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    utp, _ = UserToProblem.objects.get_or_create(problem=problem, user=request.user)
    utp.timestamp()

    solution_form = SolutionForm();

    if request.method == 'POST':
        solution_form = SolutionForm(request.POST)

        if solution_form.is_valid():
            solution = solution_form.save(commit=False)

            setattr(solution, 'user', request.user)
            setattr(solution, 'problem', problem)

            solution.save()
            #TODO przekierowac do czegoś sensownego
            return redirect('problems:problem_base')

    context = {
        'name': problem.name,
        'problem_statement': problem.problem_statement,
        'pk': pk,
        'solution_form': solution_form
    }

    return render(request, "problemBase/problemStatement.html", context)


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

    return render(request, "problemBase/problemInfo.html", context);

@login_required
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
            utp = UserToProblem();
            setattr(utp, 'user', request.user)
            setattr(utp, 'problem', created_problem)
            setattr(utp, 'is_watching', True)
            utp.save()

            return redirect('problems:problem_base')

    context = {'upload_form': upload_form}

    return render(request, "problemBase/problemUpload.html", context)
