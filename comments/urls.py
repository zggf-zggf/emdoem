from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comment/<int:pk>/<str:vote>', views.comment_vote_page, name="vote"),
    path('create_comment', views.create_comment, name="create"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete"),
]
