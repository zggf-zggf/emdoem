from django.urls import path, include
from . import views

app_name = 'solutions'
urlpatterns = [
    path('<int:pk>/solutions', views.problem_solution_page, name="solutions"),
    path('<int:pk>/<str:vote>', views.solution_vote_page, name="vote_solution"),
    path('edit/<int:pk>', views.solution_edit_page, name="edit_solution"),
    path('begin_surrender/<int:pk>/<int:as_solved>', views.begin_surrender_page, name="begin_surrender"),
    path('surrender_time/<int:pk>', views.get_surrender_time, name="surrender_time"),
    path('revert_surrender/<int:pk>', views.revert_surrender_page, name="revert_surrender"),
    path('history/<int:pk>', views.solution_history_page, name='history'),
    path('comments', include('comments.urls')),
]
