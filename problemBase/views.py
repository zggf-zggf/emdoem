from django.http import Http404
from django.shortcuts import render
from base.models import Problem, Content
from .forms import UploadForm
from django.forms import inlineformset_factory

# Create your views here.


def problem_base(request):
    problems = Problem.objects.all()
    context = {'problems': problems}
    return render(request, "problemBase/problemBase.html", context)


def problem_page(request, pk):
    problem = Problem.objects.get(pk=pk)

    if problem is not None:
        context = {'name': problem.name, 'content': problem.content, 'pk': pk}
    else:
        raise Http404("Problem does not exist!")

    return render(request, "problemBase/problemStatement.html", context)


def upload_problem_page(request):
    ProblemFormSet = inlineformset_factory(Content, Problem, fields=["name", "category"])
    content = Content.objects.get(id=3)
    form = ProblemFormSet(instance=content)
    return render(request, "problemBase/uploadProblem.html", {'form': form})