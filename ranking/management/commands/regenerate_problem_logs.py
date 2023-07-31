from django.core.management.base import BaseCommand
from ranking.models import ProblemSolvedLog
from base.models import Solution, User, Problem

class Command(BaseCommand):
    help = 'deletes all problem solved logs and generates new ones'

    def handle(self, *args, **kwargs):
        ProblemSolvedLog.objects.all().delete()
        solutions = Solution.objects.all()
        for solution in solutions:
            psl = ProblemSolvedLog(problem=solution.problem, user=solution.user)
            psl.save()
