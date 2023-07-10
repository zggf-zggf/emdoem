from django.urls import path
from . import views
app_name = 'problems'
urlpatterns = [
    path('', views.problem_base, name="problem_base"),
    path('<int:pk>', views.problem_page, name="statement"),
    path('<int:pk>/info', views.problem_page_info, name="info"),
    path('<int:pk>/solutions', views.problem_solution_page, name="solutions"),
    path('solution/<int:pk>/<str:vote>', views.vote_page, name="vote_solution"),
    path('solution/edit/<int:pk>', views.solution_edit_page, name="edit_solution"),
    path('upload', views.upload_problem_page, name="upload_problem"),
]