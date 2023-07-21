from base.models import Problem, UserToProblem, Solution, SolutionVote, Comment, CommentVote, Category
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from itertools import chain


def get_watchers_of_problem (problem):
    queryset = UserToProblem.objects.filter(problem=problem, is_watching=True).values('user')
    return list(queryset)


def get_problem_stats (problem):
    # Counts solutions with positive number of upvotes, potentially to be changed in the future
    solved = Solution.objects.filter(problem=problem).count()
    watching = UserToProblem.objects.filter(problem=problem, is_watching=True).count()
    stats = {"solved": solved, "watching": watching}
    return stats


def process_vote(solution, voter, vote):
    if voter == solution.user.username:
        return

    voters = solution.voters
    user_vote = solution.voters.get(voter) if voter in solution.voters else 0

    if user_vote == 0:
        setattr(solution, 'upvote_counter', solution.upvote_counter + vote)
        voters.update({voter: vote})

    elif vote == user_vote:
        setattr(solution, 'upvote_counter', solution.upvote_counter - vote)
        voters.pop(voter)

    setattr(solution, "voters", voters)
    solution.save()


def update_solution_upvote_counter(solution):
    solution.upvote_counter = SolutionVote.objects.filter(solution=solution).aggregate(Sum('value'))['value__sum']
    solution.save()


def update_comment_upvote_counter(comment):
    comment.upvote_counter = CommentVote.objects.filter(comment=comment).aggregate(Sum('value'))['value__sum']
    comment.save()


def get_user_stats(user):
    solutions_added = Solution.objects.filter(user=user)
    problems_added = Problem.objects.filter(added_by=user)
    comments_added = Comment.objects.filter(user=user)

    # Wybieramy rozwiązania, które mają dodatnią liczbę upvotów.
    problems_solved_solutions = Solution.objects.filter(user=user, upvote_counter__gt=0)
    problems_solved_list = []

    # Zamieniamy rozwiązania na zadania, których dotyczą.
    for solution in problems_solved_solutions:
        problems_solved_list.append(solution.problem.id)
    # Usuwamy duplikaty.
    problems_solved = Problem.objects.filter(id__in=problems_solved_list)

    stats = {
        'problems_solved': problems_solved,
        'problems_added': problems_added,
        'solutions_added': solutions_added,
        'comments_added': comments_added,
    }

    return stats


def get_categories():
    return Category.objects.all()


def solved_problem(user, problem):
    problems_solved = Solution.objects.filter(user=user, upvote_counter__gt=0)

    # Zamieniamy rozwiązania na zadania, których dotyczą.
    for solution in problems_solved:
        if solution.problem == problem:
            return True

    return False
