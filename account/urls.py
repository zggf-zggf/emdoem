from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_page, name="register"),
    path('<str:pk>', views.profile_page, name="profile_page"),
    path('<str:pk>/problems', views.user_problems_added_page, name="user_problems"),
    path('<str:pk>/solutions', views.user_solutions_added_page, name="user_solutions"),
    path('<str:pk>/comments', views.user_comments_added_page, name="user_comments"),
    path('<str:pk>/notifications', views.user_notifications_page, name="user_notifications"),
]
