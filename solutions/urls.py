from django.urls import path
from . import views

app_name = 'solutions'
urlpatterns = [
    path('<int:pk>/solutions', views.problem_solution_page, name="solutions"),
    path('solution/<int:pk>/<str:vote>', views.solution_vote_page, name="vote_solution"),
    path('solution/edit/<int:pk>', views.solution_edit_page, name="edit_solution"),
    path('begin_surrender/<int:pk>', views.begin_surrender_page, name="begin_surrender"),
    path('surrender_time/<int:pk>', views.get_surrender_time, name="surrender_time"),
    path('revert_surrender/<int:pk>', views.revert_surrender_page, name="revert_surrender"),
]
