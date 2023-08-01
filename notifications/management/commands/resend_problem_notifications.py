from django.core.management.base import BaseCommand
from base.models import Solution, User, Problem
from notifications.utils import notify_new_problem

class Command(BaseCommand):
    help = 'deletes all problem solved logs and generates new ones'

    def add_arguments(self, parser):
        parser.add_argument('problem_id', nargs='+', type=int, help='Problem ID')

    def handle(self, *args, **kwargs):
        problem_ids = kwargs['problem_id']

        for problem_id in problem_ids:
            try:
                problem = Problem.objects.get(id=problem_id)
                notify_new_problem(problem)
                self.stdout.write('Notifications send with success!')
            except Problem.DoesNotExist:
                self.stdout.write('Problem with this id doesn\'t exists')