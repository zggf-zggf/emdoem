from base.models import Problem, UserToProblem, Solution
from django.shortcuts import get_object_or_404
def get_watchers_of_problem (problem):
    queryset = UserToProblem.objects.filter(problem=problem, is_watching=True).values('user')
    return list(queryset)

def get_problem_stats (problem):
    #counts solutions with positive number of upvotes, potentially to be changed in the future
    solved= Solution.objects.filter(problem=problem, upvote_counter__gt=0).count()
    watching = UserToProblem.objects.filter(problem=problem, is_watching=True).count()
    stats = {"solved": solved, "watching": watching}
    return stats

