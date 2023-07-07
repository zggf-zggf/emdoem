from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_base, name="problem_base"),
    path('<int:pk>', views.problem_page, name="problem")
]