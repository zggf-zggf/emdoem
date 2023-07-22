from base.models import Problem, UserToProblem, Solution, SolutionVote, Comment, CommentVote, Category
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from itertools import chain
from operator import attrgetter
from django.contrib.auth import get_user_model


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

    stats = {
        'problems_solved': get_problems_solved_list(user),
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


def get_ranking():
    users = get_user_model().objects.all()

    for user in users:
        setattr(user, "user_problem_count", get_problems_solved_list(user).count())

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

    return [users, users_dictionary, user_position]


def get_problems_solved_list(user):
    # Wybieramy rozwiązania, które mają dodatnią liczbę upvotów.
    problems_solved_solutions = Solution.objects.filter(user=user, upvote_counter__gt=0)
    problems_solved_list = []

    # Zamieniamy rozwiązania na zadania, których dotyczą.
    for solution in problems_solved_solutions:
        problems_solved_list.append(solution.problem.id)
    # Usuwamy duplikaty.
    problems_solved = Problem.objects.filter(id__in=problems_solved_list)

    return problems_solved
