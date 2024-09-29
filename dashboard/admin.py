from django.contrib import admin
from dashboard.models import Question, UserQuestionnaire, Answer, Activity


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Question data view in admin panel
    """

    list_display = ["question_text", "type_name"]
    search_fields = ["question_text"]


@admin.register(UserQuestionnaire)
class UserQuestionnaireAdmin(admin.ModelAdmin):
    """
    UserQuestionnaire data view in admin panel
    """

    list_display = ["token_id", "user", "test_date"]
    search_fields = ["user"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Answer data view in admin panel
    """

    list_display = ["question", "user_questionnaire", "yes_no_answer", "text_answer"]
    search_fields = ["text_answer"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    Activity data view in admin panel
    """

    list_display = ["user", "questionnaire"]
