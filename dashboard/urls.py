from django.urls import path
from dashboard.views import ClientView, UserDetailView, SuccessQuestionnaire, RegisteredQuestionnaire \
    , DetailedQuestionnaire, SettingPage


urlpatterns = [
    path('clients/', ClientView.as_view(), name='clients'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('success/response/', SuccessQuestionnaire.as_view(), name='success_questionnaire'),
    path('registered/response/', RegisteredQuestionnaire.as_view(), name='registered_questionnaire'),
    path('detail/questionnaire/<int:id>/', DetailedQuestionnaire.as_view(), name='detail_questionnaire'),
    path('settings/', SettingPage.as_view(), name='settings'),
]
