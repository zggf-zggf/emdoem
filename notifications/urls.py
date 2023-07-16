from django.urls import path
from . import views
app_name = 'notifications'

urlpatterns = [
    path("read_all", views.read_all_notifications, name="read_all"),
]
