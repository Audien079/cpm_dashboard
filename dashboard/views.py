from django.urls import reverse_lazy
from users.models import User
from django.views.generic import ListView, TemplateView


class ClientView(ListView):
    """
    Client view
    """
    login_url = reverse_lazy("login")
    template_name = "dashboard/client.html"
    model = User
    queryset = User.objects.all().order_by("id").filter(is_admin=False)
    context_object_name = "users"


class UserDetailView(ListView):
    """
    User detail view
    """
    login_url = reverse_lazy("login")
    template_name = "users/profile.html"
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
