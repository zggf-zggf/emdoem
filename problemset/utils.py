from base.models import Problem
from problembase.utils import add_status_to_problems
import json

def process_problemset_json(json, user):
    for row in json:
        if row['type'] == 'problem':
            process_problem_object(row, user)

def process_problem_object(obj, user):
    problem = Problem.objects.filter(pk=obj['id']).first()
    if problem is None:
        obj['valid'] = False
        obj['name'] = "Bład - takie zadanie nie istnieje"
    else:
        obj['valid'] = True
        if not 'name' in obj:
            obj['name'] = problem.name
        add_status_to_problems([problem], user)
        obj['status'] = getattr(problem, 'status', None)