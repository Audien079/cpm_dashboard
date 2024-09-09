from django.urls import reverse_lazy
from users.models import User
from django.views.generic import ListView, TemplateView


class DashboardView(ListView):
    """
    Dashboard view
    """
    login_url = reverse_lazy("login")
    template_name = "dashboard/dashboard.html"
    model = User
    queryset = User.objects.all().order_by("id")
    context_object_name = "users"


class UserDetailView(ListView):
    """
    User detail view
    """
    login_url = reverse_lazy("login")
    template_name = "dashboard/user_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["id"])
        all_questionnaires = user.user_questionnaires.order_by("-created_at").all()
        latest_questionnaire = all_questionnaires.order_by("-created_at").filter(is_completed=True).first()

        if latest_questionnaire:
            context["answers"] = latest_questionnaire.questionnaire_answers.all()

        context["questionnaires"] = all_questionnaires
        context["user"] = user
        return context


class SuccessQuestionnaire(TemplateView):
    """
    Success page to redirect to user
    """
    template_name = "dashboard/success_questionnaire.html"
