from django.shortcuts import render
from base.utils import get_ranking

# Create your views here.


def ranking_page(request):
    ranking = get_ranking()

    context = {
        'users_ranking': ranking[0],
        'problems_solved_count': ranking[1]
    }

    return render(request, 'ranking/ranking_page.html', context)

