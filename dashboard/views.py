from django.urls import reverse_lazy
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from dashboard.models import Activity, UserQuestionnaire, Question


class ClientView(LoginRequiredMixin, ListView):
    """
    Client view
    """
    login_url = reverse_lazy("login")
    template_name = "dashboard/client.html"
    model = User
    queryset = User.objects.all().order_by("id").filter(is_admin=False)
    context_object_name = "users"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     from dashboard.models import UserQuestionnaire
    #     import os
    #     from dashboard.utils import email_questionnaire
    #     user_obj = User.objects.filter(pk=3).first()
    #
    #     questionnaire = UserQuestionnaire.objects.create(user=user_obj)
    #     Activity.objects.create(user=user_obj, questionnaire=questionnaire)
    #     questionnaire_link = os.environ.get("SITE_URL") + f'/questionnaire/{questionnaire.id}/'
    #     email_questionnaire(user_obj, questionnaire_link)


class UserDetailView(LoginRequiredMixin, ListView):
    """
    User detail view
    """
    login_url = reverse_lazy("login")
    template_name = "dashboard/user_detail_new.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["id"])
        activities = Activity.objects.filter(user=user).order_by("-created_at")
        all_questionnaires = user.user_questionnaires.order_by("-created_at").all()
        latest_questionnaire = all_questionnaires.order_by("-created_at").filter(is_completed=True).first()

        if latest_questionnaire:
            context["answers"] = latest_questionnaire.questionnaire_answers.all()

        context["questionnaires"] = all_questionnaires
        context["activities"] = activities
        context["user"] = user

        search = self.request.GET.get("search")
        if search:
            context["answers"] = latest_questionnaire.questionnaire_answers.filter(question__question_text__icontains=search)

        return context


class SuccessQuestionnaire(TemplateView):
    """
    Success page to redirect to user
    """
    template_name = "dashboard/success_questionnaire.html"


class RegisteredQuestionnaire(TemplateView):
    """
    Success page to redirect to user
    """
    template_name = "dashboard/registered_questionnaire.html"


class DetailedQuestionnaire(TemplateView):
    """
    Success page to redirect to user
    """
    template_name = "dashboard/detail_questionnaire.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionnaire = UserQuestionnaire.objects.get(id=self.kwargs["id"])
        sections = Question.objects.filter(parent_question__isnull=True).order_by('id')
        context["questionnaire"] = questionnaire
        context["sections"] = sections
        return context
