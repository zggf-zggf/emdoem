from base.models import User, Problem, UserToProblem, Solution
from .models import ProblemSolvedLog
from django.contrib.auth import get_user_model
from base.utils import get_problems_solved_list
from itertools import chain
from operator import attrgetter


def notify_problem_solved(problem, user):
    if not ProblemSolvedLog.objects.filter(problem=problem, user=user).exists():
        psl = ProblemSolvedLog(problem=problem, user=user)
        psl.save()


def get_ranking(pk):
    users = get_user_model().objects.all()

    for user in users:
        setattr(user, "user_problem_count", get_problems_solved_list(user, pk).count())

    users = sorted(
        chain(users),
        key=attrgetter('user_problem_count'),
        reverse=True
    )

    users_dictionary = {}
    user_position = {}

    previous_count = -1
    user_count = 1
    position = 0

    for user in users:
        if previous_count != user.user_problem_count:
            position = user_count
            previous_count = user.user_problem_count

        user_count += 1

        users_dictionary[user] = user.user_problem_count
        user_position[user] = position

    problem_solved_logs = ProblemSolvedLog.objects.all().order_by('date')[:7]
    ranking = {}
    ranking = {
        'users_ranking': users,
        'problems_solved_count': users_dictionary,
        'user_position': user_position,
        'problem_solved_logs': problem_solved_logs,
    }
    return ranking

