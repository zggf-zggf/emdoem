from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.response import TemplateResponse

from notifications.views import show_notifications
from .forms import ProblemsetForm
from .models import Problemset
from .utils import process_problemset_json


# Create your views here.
@show_notifications
@login_required(login_url='account:login')
def problemset_create_page(request):
    form = ProblemsetForm()

    if request.method == 'POST':
        form = ProblemsetForm(request.POST)

        if form.is_valid():
            problemset = form.save(commit=False)

            setattr(problemset, "user", request.user)
            problemset.save()

            return redirect('problemset:edit', pk=problemset.pk)

    context = {'form': form}

    return TemplateResponse(request, "problemset/problemsetCreate.html", context)

@show_notifications
@login_required(login_url='account:login')
def problemset_edit_basic_page(request, pk):
    problemset = get_object_or_404(Problemset, pk=pk)

    if request.user != problemset.user:
        raise PermissionDenied()

    form = ProblemsetForm(request.POST or None, instance=problemset)
    if form.is_valid():
        problemset = form.save(commit=False)
        problemset.save()
        return redirect('problemset:edit', pk=problemset.id)

    context = {
        'form': form,
    }
    return TemplateResponse(request, "problemset/problemsetCreate.html", context)

@show_notifications
@login_required(login_url='account:login')
def problemset_edit_page(request, pk):
    problemset = get_object_or_404(Problemset, pk=pk)
    if problemset.user != request.user:
        raise PermissionDenied()

    json = problemset.content
    process_problemset_json(json)
    print(json)
    context = {
        'problemset': problemset,
        'rows': json,
    }
    return TemplateResponse(request, "problemset/problemsetEdit.html", context)
