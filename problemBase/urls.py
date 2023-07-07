from django.urls import path
from . import views
app_name = 'problems'
urlpatterns = [
    path('', views.problem_base, name="problem_base"),
    path('<int:pk>', views.problem_page, name="statement"),
    path('upload', views.upload_problem_page, name="upload_problem"),
]