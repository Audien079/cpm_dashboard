from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from users.views import CustomLoginView, SignUpView, SendQuestionnaire, send_email_questionnaire\
    , modify_user_address, modify_user_dob, modify_user_email, modify_user_phone, AdminUsersView\
    , save_questions, CompleteQuestionnaire


urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=False), name="dashboard-redirect"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/admin/", AdminUsersView.as_view(), name="admin_users"),
    path("questionnaire/<int:pk>/", SendQuestionnaire.as_view(), name="send_questionnaire"),
    path("email/questionnaire/", send_email_questionnaire, name="email_questionnaire"),
    path("modify/address/", modify_user_address, name="modify_user_address"),
    path("modify/date_of_birth/", modify_user_dob, name="modify_user_dob"),
    path("modify/email/", modify_user_email, name="modify_user_email"),
    path("modify/phone/", modify_user_phone, name="modify_user_phone"),
    path("save/questions/", save_questions, name="save_questions"),
    path("complete/questionnaire/", CompleteQuestionnaire.as_view(), name="complete_questionnaire"),
]
