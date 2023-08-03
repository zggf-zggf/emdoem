from django.urls import path, include
from . import views
from .views import ProblemBaseView
app_name = 'problems'
urlpatterns = [
    path('', ProblemBaseView.as_view(template_name="problembase/problembase.html"), name="problem_base"),
    path('<int:pk>', views.problem_page, name="statement"),
    path('<int:pk>/info', views.problem_page_info, name="info"),
    path('comment/<int:pk>/<str:vote>', views.comment_vote_page, name="vote_comment"),
    path('create_comment', views.create_comment, name="create_comment"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete_comment"),
    path('upload', views.upload_problem_page, name="upload_problem"),
    path('watch/<int:pk>', views.watch_problem_page, name="watch_problem"),
]