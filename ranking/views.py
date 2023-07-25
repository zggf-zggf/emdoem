from django.shortcuts import render
from .utils import get_ranking
from base.models import Category

# Create your views here.


def ranking_page(request):
    ranking = get_ranking('')
    categories = Category.objects.all()

    context = ranking
    context['categories'] = categories

    return render(request, 'ranking/ranking_page.html', context)


def ranking_selected(request, pk):
    ranking = get_ranking(pk)
    categories = Category.objects.all()

    context = ranking
    context['categories'] = categories

    return render(request, 'ranking/ranking_page.html', context)
