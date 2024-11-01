from django.urls import path
from dashboard.views import HomeView, UserDetailView, SuccessQuestionnaire, RegisteredQuestionnaire \
    , DetailedQuestionnaire, ClientsPage, create_task, complete_task, uncomplete_task, edit_task


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('success/response/', SuccessQuestionnaire.as_view(), name='success_questionnaire'),
    path('registered/response/', RegisteredQuestionnaire.as_view(), name='registered_questionnaire'),
    path('detail/questionnaire/<int:id>/', DetailedQuestionnaire.as_view(), name='detail_questionnaire'),
    path('clients/', ClientsPage.as_view(), name='clients'),
    path('create/task/', create_task, name='create_task'),
    path('complete/task/', complete_task, name='complete_task'),
    path('uncomplete/task/', uncomplete_task, name='uncomplete_task'),
    path('edit/task/', edit_task, name='edit_task'),
]
