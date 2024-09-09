from django.urls import path
from dashboard.views import DashboardView, UserDetailView, SuccessQuestionnaire


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('success/response/', SuccessQuestionnaire.as_view(), name='success_questionnaire'),
]
