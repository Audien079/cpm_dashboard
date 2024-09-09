import os
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import customRegistrationForm
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from dashboard.models import UserQuestionnaire, Question, Answer
from dashboard.utils import email_questionnaire
from users.models import User


class CustomLoginView(LoginView):
    """
    Login view
    """
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')


class SignUpView(CreateView):
    """
    Sign up view
    """
    login_url = 'login'
    template_name = 'user/register.html'
    form_class = customRegistrationForm

    def post(self, request):
        form = customRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
        else:
            return render(request, self.template_name, context={'form': form})


class SendQuestionnaire(TemplateView):
    """
    Sends questionare to user
    """
    template_name = 'user/send_questions.html'

    def get_queryset(self):
        question_id = self.kwargs.get("pk")
        return UserQuestionnaire.objects.filter(id=question_id)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["questions"] = Question.objects.all()
        context_data["questionnire"] = self.kwargs.get("pk")
        return context_data


class SaveQuestionnaire(View):
    """
    Save Questionnaire
    """

    def post(self, request):
        data = request.POST
        questionnaire_id = request.GET.get("qnr")
        questionnaire = UserQuestionnaire.objects.get(id=questionnaire_id)
        data_keys = data.keys()
        for key in data_keys:
            if key.startswith("qn"):
                question = Question.objects.get(id=key[3:])

                if data[key] == "yes":
                    yn = True
                else:
                    yn = False

                Answer.objects.create(
                    user_questionnaire=questionnaire,
                    question=question,
                    yes_no_answer=yn
                )
        questionnaire.is_completed = True
        questionnaire.test_date = datetime.now()
        questionnaire.save()
        return redirect(reverse('success_questionnaire'))


@require_POST
def send_email_questionnaire(request):
    """
    Send questionnaire to user using email
    """
    if request.method != "POST" and not request.is_ajax():
        return JsonResponse({"message": "Request method is not valid"})

    user_obj = User.objects.filter(pk=request.POST.get("pk")).first()

    if not user_obj:
        return JsonResponse({"message": "No Record Found"})

    questionnaire = UserQuestionnaire.objects.filter(user=user_obj, is_completed=False)
    if questionnaire.count() > 0:
        return JsonResponse({"message": "failure", "data": "User already had unanswered questionnaire"})

    questionnaire = UserQuestionnaire.objects.create(user=user_obj)
    questionnaire_link = os.environ.get("SITE_URL") + f'/questionnaire/{questionnaire.id}/'
    email_questionnaire(user_obj, questionnaire_link)
    return JsonResponse({"message": "success", "data": "Removed Successfully"})
