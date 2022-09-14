from django.urls import path
from .views import dashboard, profile, Checkprofile
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


app_name = "utilisateurs"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="utilisateurs/login.html",
                                     authentication_form=LoginForm), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", dashboard, name="dashboard"),
    path("profile", profile, name="profile"),
    path("checkprofile/", Checkprofile.as_view, name="checkprofile")
]
