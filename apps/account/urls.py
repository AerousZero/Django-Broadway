from django.urls import path
from .views import UserRegistrationView, UserLoginView, user_logout

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/",UserLoginView.as_view(), name="user_login"),
    path("login/", user_logout, name="user_logout")
]
