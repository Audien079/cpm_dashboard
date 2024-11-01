from datetime import datetime
from django.urls import reverse_lazy
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from dashboard.models import Activity, UserQuestionnaire, Question
from django.http import JsonResponse
from users.models import Task


class ClientsPage(LoginRequiredMixin, ListView):
    """
    Home view
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
    #     user_obj = User.objects.filter(pk=4).first()
    #
    #     questionnaire = UserQuestionnaire.objects.create(user=user_obj)
    #     Activity.objects.create(user=user_obj, questionnaire=questionnaire)
    #     questionnaire_link = os.environ.get("SITE_URL") + f'/questionnaire/{questionnaire.id}/'
    #     email_questionnaire(user_obj, questionnaire_link)


class HomeView(TemplateView):
    """
    Clients page
    """
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questionnaires"] = UserQuestionnaire.objects.all()
        context["completed_tasks"] = Task.objects.filter(is_completed=True)
        context["pending_tasks"] = Task.objects.filter(is_completed=False)
        context["users"] = User.objects.filter(is_admin=False)
        return context


def create_task(request):
    """
    Create task
    """
    if request.method == 'POST':
        client = request.POST.get('client')
        task_name = request.POST.get('task_name')
        due_date = request.POST.get('due_date')
        details = request.POST.get('details')
        user = User.objects.get(id=client)

        Task.objects.create(
            client=user,
            name=task_name,
            due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
            details=details
        )
        return redirect(reverse('home') + '?done=true')


def complete_task(request):
    """
    Mark task as completed
    """
    task_id = request.POST.get("task_id")
    task = Task.objects.get(id=task_id)
    task.is_completed = True
    task.completed_on = datetime.now().date()
    task.save()
    return JsonResponse({"message": "success"})


def uncomplete_task(request):
    """
    Mark task as not completed
    """
    task_id = request.POST.get("task_id")
    task = Task.objects.get(id=task_id)
    task.is_completed = False
    task.save()
    return JsonResponse({"message": "success"})


def edit_task(request):
    """
    Edit task completed
    """
    task_id = request.POST.get("task_id")
    date_str = request.POST.get("updated_due_date")
    task = Task.objects.get(id=task_id)
    due_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    task.due_date = due_date
    task.save()
    return JsonResponse({"message": "success", "due_date": due_date.strftime("%m/%d/%Y")})


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
        activities = Activity.objects.filter(user=user).order_by("-questionnaire__created_at")
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

        # Fetch all related answers and prefetch related questions and parent questions in one go
        answers = list(
            questionnaire.questionnaire_answers.select_related('question__parent_question')
            .values('id', 'user_questionnaire_id', 'question_id', 'question__parent_question_id',
                    'question__question_text', 'question__order', 'yes_no_answer', 'text_answer')
            .order_by('id')
        )
        current_date = datetime.now()
        formatted_date = current_date.strftime("%m/%d/%Y")

        # Section headers based on question order
        section_headers = {
            '1': "+ Section 1  Contact Information",
            '2': "+ Section 2  Tax Return",
            '3': "+ Section 3  Change in Business",
            '4': "+ Section 4  Change in personal financial life"
        }

        output_list = []

        # First pass: build the output list for the main questions (order 1 to 4)
        for answer in answers:
            answer["yes_no_answer"] = answer["yes_no_answer"].capitalize()
            if answer['question__order'] in section_headers:
                output_dict = {
                    "id": answer["id"],
                    "user_questionnaire_id": answer["user_questionnaire_id"],
                    "question_id": answer["question_id"],
                    "yes_no_answer": answer["yes_no_answer"].capitalize(),
                    "text_answer": answer["text_answer"],
                    "question": answer["question__question_text"].replace("[today]", formatted_date),
                    "order": answer["question__order"],
                    "header": section_headers[answer['question__order']],
                    "childrens": []
                }
                output_list.append(output_dict)

        # Second pass: assign children to their parent questions
        for output in output_list:
            for answer in answers:
                if (answer["question__parent_question_id"] == output["question_id"] and
                        output["yes_no_answer"].lower() != "no"):
                    output["childrens"].append(answer)

        context["data"] = output_list
        return context
