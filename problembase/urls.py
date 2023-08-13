from django.urls import path, include
from . import views
from .views import ProblemBaseView
app_name = 'problems'
urlpatterns = [
    path('', ProblemBaseView.as_view(template_name="problembase/problemBase.html"), name="problem_base"),
    path('<int:pk>', views.problem_page, name="statement"),
    path('<int:pk>/info', views.problem_page_info, name="info"),
    path('upload', views.upload_problem_page, name="upload_problem"),
    path('<int:pk>/edit', views.problem_edit_page, name="edit_problem"),
    path('watch/<int:pk>', views.watch_problem_page, name="watch_problem"),
    path('history/<int:pk>', views.problem_history_page, name='history'),
    path('upload_api', views.upload_problem_api, name='upload_api'),
    path('problem_statement_api/<int:pk>', views.problem_statement_api, name='problem_statement_api'),
]