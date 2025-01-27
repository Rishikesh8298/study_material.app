from django.urls import path
from .views import signin, signup, user_logout, change_password

urlpatterns = [
    path("signin/", signin, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", user_logout, name="logout"),
    path("change-password/", change_password, name="change_password"),
]
