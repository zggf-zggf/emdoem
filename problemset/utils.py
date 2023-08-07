from base.models import Problem
import json

def process_problemset_json(json):
    print(json[0]['type'])
    for row in json:
        if row['type'] == 'problem':
            process_problem_object(row)

def process_problem_object(obj):
    problem = Problem.objects.filter(pk=obj['id']).first()
    if problem is None:
        obj['valid'] = False
        obj['name'] = "Bład - takie zadanie nie istnieje"
    else:
        obj['valid'] = True
        if not 'name' in obj:
            obj['name'] = problem.name
