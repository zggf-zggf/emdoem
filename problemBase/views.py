from django.http import Http404
from django.shortcuts import render
from base.models import Problem

# Create your views here.


def problem_base(request):
    problems = Problem.objects.all()
    context = {'problems': problems}
    return render(request, "problemBase/problemBase.html", context)


def problem_page(request, pk):
    problem = Problem.objects.get(pk=pk)

    if problem is not None:
        context = {'name': problem.name, 'content': problem.content}
    else:
        raise Http404("Problem does not exist!")

    return render(request, "problemBase/problem.html", context)
