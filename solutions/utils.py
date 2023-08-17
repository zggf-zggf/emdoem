from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from itertools import chain
from operator import attrgetter
from problembase.utils import has_user_solved_problem

from base.models import Problem, UserToProblem, Solution, SolutionVote, Comment, CommentVote, Category


def update_solution_upvote_counter(solution):
    solution.upvote_counter = SolutionVote.objects.filter(solution=solution).aggregate(Sum('value'))['value__sum']
    solution.save()

def can_see_solutions(user, problem):
    utp, _ = UserToProblem.objects.get_or_create(user=user, problem=problem)
    return has_user_solved_problem(user, problem) or utp.surrendered
