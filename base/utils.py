from base.models import Problem, UserToProblem, Solution
from django.shortcuts import get_object_or_404


def get_watchers_of_problem (problem):
    queryset = UserToProblem.objects.filter(problem=problem, is_watching=True).values('user')
    return list(queryset)


def get_problem_stats (problem):
    # Counts solutions with positive number of upvotes, potentially to be changed in the future
    solved= Solution.objects.filter(problem=problem, upvote_counter__gt=0).count()
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
