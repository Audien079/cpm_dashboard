from django.urls import path
from dashboard.views import HomeView, UserDetailView, SuccessQuestionnaire, RegisteredQuestionnaire \
    , DetailedQuestionnaire, ClientsPage


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('success/response/', SuccessQuestionnaire.as_view(), name='success_questionnaire'),
    path('registered/response/', RegisteredQuestionnaire.as_view(), name='registered_questionnaire'),
    path('detail/questionnaire/<int:id>/', DetailedQuestionnaire.as_view(), name='detail_questionnaire'),
    path('clients/', ClientsPage.as_view(), name='clients'),
]
