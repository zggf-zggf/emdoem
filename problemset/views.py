from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.list import ListView

from base.models import Problem
from notifications.views import show_notifications
from .forms import ProblemsetForm
from .models import Problemset
from .utils import process_problemset_json
from problembase.utils import add_stats_to_problems, add_status_to_problems


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

class ProblemSearchResults(ListView):
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
