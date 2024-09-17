from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from users.views import CustomLoginView, SignUpView, SendQuestionnaire, SaveQuestionnaire, send_email_questionnaire\
    , modify_user_address, modify_user_dob, modify_user_email, modify_user_phone, AdminUsersView


urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=False), name="dashboard-redirect"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/admin/", AdminUsersView.as_view(), name="admin_users"),
    path("questionnaire/<int:pk>/", SendQuestionnaire.as_view(), name="send_questionnaire"),
    path("saveqestionnaire/", SaveQuestionnaire.as_view(), name="save_questionnaire"),
    path("email/questionnaire/", send_email_questionnaire, name="email_questionnaire"),
    path("modify/address/", modify_user_address, name="modify_user_address"),
    path("modify/date_of_birth/", modify_user_dob, name="modify_user_dob"),
    path("modify/email/", modify_user_email, name="modify_user_email"),
    path("modify/phone/", modify_user_phone, name="modify_user_phone"),
]
