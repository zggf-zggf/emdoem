from django.shortcuts import render
from base.models import Problem

# Create your views here.


def problem_base(request):
    problems = Problem.objects.all()
    context = {'problems': problems}
    return render(request, "problemBase.html", context)
