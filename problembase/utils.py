from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from itertools import chain
from operator import attrgetter

from base.models import Problem, UserToProblem, Solution, SolutionVote, Comment, CommentVote, Category


def get_categories():
    return Category.objects.all()

def get_watchers_of_problem (problem):
    queryset = UserToProblem.objects.filter(problem=problem, is_watching=True).values('user')
    return list(queryset)


def get_problem_stats (problem):
    # Counts solutions with positive number of upvotes, potentially to be changed in the future
    solved = Solution.objects.filter(problem=problem).count()
    watching = UserToProblem.objects.filter(problem=problem, is_watching=True).count()
    stats = {"solved": solved, "watching": watching}
    return stats


def add_stats_to_problems (problems):
    for problem in problems:
        stats = get_problem_stats(problem)
        setattr(problem, "watchers_count", stats["watching"])
        setattr(problem, "solved", stats["solved"])

def add_status_to_problems (problems, user):
    if not user.is_authenticated:
        return

    for problem in problems:
        #https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist-in-django
        utp = UserToProblem.objects.filter(user=user, problem=problem).first()
        if utp is not None:
            if has_user_solved_problem(user, problem):
                setattr(problem, 'status', 'solved')
            elif utp.surrendered:
                setattr(problem, 'status', 'surrendered')
            else:
                setattr(problem, 'status', 'visited')


def has_user_solved_problem(user, problem):
    problems_solved = Solution.objects.filter(user=user, upvote_counter__gte=0)

    for solution in problems_solved:
        if solution.problem == problem:
            return True

    return False


def get_problems_solved_list(user, category_pk=''):
    if category_pk == '':
        problems_solved_solutions = Solution.objects.filter(user=user)
    else:
        problems_solved_solutions = Solution.objects.filter(user=user, problem__category_id=category_pk)

    problems_solved_list = []

    # Zamieniamy rozwiązania na zadania, których dotyczą.
    for solution in problems_solved_solutions:
        problems_solved_list.append(solution.problem.id)
    # Usuwamy duplikaty.
    problems_solved = Problem.objects.filter(id__in=problems_solved_list)

    return problems_solved

def get_user_stats(user):
    solutions_added = Solution.objects.filter(user=user)
    problems_added = Problem.objects.filter(added_by=user)
    comments_added = Comment.objects.filter(user=user)

    stats = {
        'problems_solved': get_problems_solved_list(user, ''),
        'problems_added': problems_added,
        'solutions_added': solutions_added,
        'comments_added': comments_added,
    }

    return stats

