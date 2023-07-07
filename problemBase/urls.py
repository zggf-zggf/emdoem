from django.urls import path
from . import views
app_name = 'problems'
urlpatterns = [
    path('', views.problem_base, name="problem_base"),
    path('<int:pk>', views.problem_page, name="problem")
]