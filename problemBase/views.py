from django.http import Http404
from django.shortcuts import render, redirect
from base.models import Problem
from .forms import UploadForm
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

    context = {'name': problem.name,
                'problem_statement': problem.problem_statement,
                'pk': pk}

    return render(request, "problemBase/problemStatement.html", context)

@login_required
def problem_page_info(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    context = {'name': problem.name,
               'pk': pk,
               'problem_statement': problem.problem_statement,
               'added_by': problem.added_by,
               'creation_date': problem.creation_date,
                'category': problem.category}

    return render(request, "problemBase/problemInfo.html", context);


# To do: uploadowanie zdjęcia z poziomu strony, a nie przez panel admina.
@login_required
def upload_problem_page(request):
    upload_form = UploadForm()

    if request.method == 'POST':
        upload_form = UploadForm(request.POST)

        if upload_form.is_valid() and \
                (upload_form['content_text'].value() is not None or upload_form['image'].value() is not None):

            print(upload_form['content_text'].value())
            problem = upload_form.save(commit=False)

            problem.save()
            return redirect('problems:problem_base')

    context = {'upload_form': upload_form}

    return render(request, "problemBase/problemUpload.html", context)
