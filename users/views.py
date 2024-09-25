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
from django.views.generic import TemplateView, View, ListView
from dashboard.models import UserQuestionnaire, Question, Answer
from dashboard.utils import email_questionnaire
from users.models import User
from users.utils import is_valid_email


class CustomLoginView(LoginView):
    """
    Login view
    """
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('clients')


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

    def get(self, request, *args, **kwargs):
        questionnaire = UserQuestionnaire.objects.filter(id=self.kwargs.get("pk")).first()
        if questionnaire.is_completed:
            return redirect('registered_questionnaire')
        else:
            return super().get(request, *args, **kwargs)

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


class AdminUsersView(ListView):
    """
    Admin Users view
    """
    login_url = reverse_lazy("login")
    template_name = "users/admin_users.html"
    model = User
    queryset = User.objects.all().order_by("id").filter(is_admin=True)
    context_object_name = "users"


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


@require_POST
def modify_user_address(request):
    """
    Modify user address
    """
    if request.method != "POST" and not request.is_ajax():
        return JsonResponse({"message": "Request method is not valid"})

    updated_address = request.POST.get("updated_address")
    user_id = request.POST.get("user_id")
    user = User.objects.get(id=user_id)

    if user.address == updated_address:
        return JsonResponse({"message": "failure", "data": "New address is same as old address"})

    user.address = updated_address
    user.save()
    return JsonResponse({"message": "success", "data": "New address is saved"})


@require_POST
def modify_user_dob(request):
    """
    Modify user date of birth
    """
    if request.method != "POST" and not request.is_ajax():
        return JsonResponse({"message": "Request method is not valid"})

    updated_dob = request.POST.get("updated_dob")
    user_id = request.POST.get("user_id")
    user = User.objects.get(id=user_id)
    updated_dob = datetime.strptime(updated_dob, "%Y-%m-%d")
    current_date = datetime.now().date()

    if updated_dob.date() > current_date:
        return JsonResponse({"message": "failure", "data": "Future date can't be selected"})

    if user.date_of_birth == updated_dob:
        return JsonResponse({"message": "failure", "data": "New date of birth is same as old date of birth"})

    user.date_of_birth = updated_dob
    user.save()
    updated_dob = datetime.strftime(updated_dob.date(), "%m/%d/%Y")
    return JsonResponse({"message": "success", "data": "New date of birth is saved", "dob": updated_dob})


@require_POST
def modify_user_email(request):
    """
    Modify user email
    """
    if request.method != "POST" and not request.is_ajax():
        return JsonResponse({"message": "Request method is not valid"})

    updated_email = request.POST.get("updated_email")

    is_valid = is_valid_email(updated_email)

    if not is_valid:
        return JsonResponse({"message": "failure", "data": "Email is not valid"})

    user_id = request.POST.get("user_id")
    user = User.objects.get(id=user_id)

    if user.email == updated_email:
        return JsonResponse({"message": "failure", "data": "New email is same as old email"})

    user.email = updated_email
    user.save()
    return JsonResponse({"message": "success", "data": "New email is saved"})


@require_POST
def modify_user_phone(request):
    """
    Modify user phone
    """
    if request.method != "POST" and not request.is_ajax():
        return JsonResponse({"message": "Request method is not valid"})

    updated_phone = request.POST.get("updated_phone").replace('-', '')

    # is_valid = is_valid_email(updated_email)
    #
    # if not is_valid:
    #     return JsonResponse({"message": "failure", "data": "Phone number is not valid"})

    user_id = request.POST.get("user_id")
    user = User.objects.get(id=user_id)

    if user.phone == updated_phone:
        return JsonResponse({"message": "failure", "data": "New phone number is same as old phone number"})

    user.phone = updated_phone
    user.save()
    return JsonResponse({"message": "success", "data": "New phone number is saved"})
