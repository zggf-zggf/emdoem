from django.urls import path, include
from . import views

app_name = 'problemset'
urlpatterns = [
    path('create/', views.problemset_create_page, name='create'),
    path('edit_basic/<int:pk>/', views.problemset_edit_basic_page, name='edit_basic'),
    path('edit/<int:pk>/', views.problemset_edit_page, name='edit'),
    path('search_problem/', views.ProblemSearchResults.as_view(template_name="problemset/_problemSearchResults.html"), name='search_problem'),
    path('editable_problem_entry/<int:pk>', views.EditableProblemEntry, name='editable_problem_entry'),
    path('save/<int:pk>', views.ProblemsetSave, name='save'),
    path('<int:pk>', views.ProblemsetView, name='problemset'),
    path('problem/<int:problemset_pk>/<int:problem_pk>', views.ProblemInProblemset, name='problem_in_problemset'),
]
