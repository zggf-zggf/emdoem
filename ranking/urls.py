from django.urls import path
from . import views


app_name = 'ranking'
urlpatterns = [
    path('', views.ranking_page, name="ranking"),
    path('<int:pk>', views.ranking_selected, name="ranking-selected"),
]
