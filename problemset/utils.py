from base.models import Problem, UserToProblem
from problembase.utils import add_status_to_problems
import json
import random
from .models import ProblemsetDuringEditing, UserToProblemset

def process_problemset_content(content, user):
    print("processing...")
    for row in content:
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

def problem_in_problemset_preview(problem, problemset, user):
    rows = problemset.content
    process_problemset_content(rows, user)
    rows = list(filter(lambda row: row['type'] != 'comment', rows))
    i = 0
    idx = 0
    for row in rows:
        if row['type'] == 'problem' and row['id'] == problem.id:
            idx = i
            row['selected'] = True
        i += 1
    rows = rows[max(idx - 3, 0):min(idx + 4, len(rows))]
    problemset_data = {
        'id': problemset.id,
        'name': problemset.name,
        'rows': rows,
        'more_before': idx - 3 > 0,
        'more_ahead': idx + 4 < len(problemset.content)-1,
    }
    return problemset_data

def get_problemset_progress(problemset, user):
    utpset, _ = UserToProblemset.objects.get_or_create(problemset=problemset, user=user)
    total = 0
    solved = 0
    surrendered = 0
    print(utpset.is_progress_valid())
    if not utpset.is_progress_valid():
        process_problemset_content(problemset.content, user)
        processed_content = problemset.content
        for row in processed_content:
            if row['type'] =='problem':
               total += 1
               if row['status'] == 'solved':
                   solved += 1
               elif row['status'] == 'surrendered':
                   surrendered += 1
        utpset.total_count = total
        utpset.solved_count = solved
        utpset.surrendered_count = surrendered
        utpset.save()
    else:
        total = utpset.total_count
        solved = utpset.solved_count
        surrendered = utpset.surrendered_count

    if total != 0:
        return {
            'total': total,
            'solved': solved,
            'surrendered': surrendered,
            'solved_amount': 100 * solved / total,
            'surrendered_amount': 100 * surrendered / total,
        }
    else:
        return {
            'total': 0,
            'solved_amount': 0,
            'surrendered_amount': 0,
        }

def attach_problemset_progress(problemset, user):
    problemset.progress = get_problemset_progress(problemset, user)

def get_motivation_on_progress(progress):
    if progress == 0:
        return random.choice(['Świeży zbiorek, coś pięknego!'])
    elif progress < 20:
       return random.choice(['Dobry start', 'Ładnie', 'Nieźle', 'Nice', 'Pan tak szybko?', 'Czas na kolejne'])
    elif progress < 60:
        return random.choice(['Idziesz jak burza', 'Cios za ciosem', 'Nieźle', 'Nice', 'Już tyle?', 'Czas na kolejne', 'Przygotowania pełną parą'])
    elif progress < 95:
        return random.choice(['Najtrudniejsze na koniec', 'Co to dla ciebie', 'Nieźle', 'Nice', 'Prawie zdane', 'Przygotowania pełną parą'])
    else:
        return random.choice(['Kox', 'PRO', 'Destrukcja', 'Brawo!'])

def get_basic_problemset_data_for_problem(problem, user):
    utp, _ = UserToProblem.objects.get_or_create(user=user, problem=problem)
    if utp.seen_in_problemset:
        return {'id': utp.seen_in_problemset.id}
    else:
        return None

def register_problemset_editing_notification(user, problemset):
   pde, _ = ProblemsetDuringEditing.objects.get_or_create(user=user)
   pde.problemset = problemset
   pde.save()
def unregister_problemset_editing_notification(user):
    pde, _ = ProblemsetDuringEditing.objects.get_or_create(user=user)
    pde.problemset = None
    pde.save()

def check_for_problemset_editing_notification(user):
    pde, _ = ProblemsetDuringEditing.objects.get_or_create(user=user)
    if pde.problemset:
        return {'id': pde.problemset.id}
    else:
        return None