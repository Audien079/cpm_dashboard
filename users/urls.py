from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from users.views import CustomLoginView, SignUpView, SendQuestionnaire, SaveQuestionnaire, send_email_questionnaire


urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=False), name="dashboard-redirect"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("questionnaire/<int:pk>/", SendQuestionnaire.as_view(), name="send_questionnaire"),
    path("saveqestionnaire/", SaveQuestionnaire.as_view(), name="save_questionnaire"),
    path("email/questionnaire/", send_email_questionnaire, name="email_questionnaire")
]
