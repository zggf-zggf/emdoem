from django.urls import path, include
from . import views

app_name = 'problemset'
urlpatterns = [
    path('create/', views.problemset_create_page, name='create'),
    path('edit_basic/<int:pk>/', views.problemset_edit_basic_page, name='edit_basic'),
    path('edit/<int:pk>/', views.problemset_edit_page, name='edit'),
]
