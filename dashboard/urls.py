from django.urls import path
from dashboard.views import ClientView, UserDetailView, SuccessQuestionnaire, RegisteredQuestionnaire


urlpatterns = [
    path('clients/', ClientView.as_view(), name='clients'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('success/response/', SuccessQuestionnaire.as_view(), name='success_questionnaire'),
    path('registered/response/', RegisteredQuestionnaire.as_view(), name='registered_questionnaire'),
]
