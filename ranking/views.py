from django.shortcuts import render
from .utils import get_ranking

# Create your views here.


def ranking_page(request):
    ranking = get_ranking()

    context = ranking

    return render(request, 'ranking/ranking_page.html', context)

