from uuid import uuid4
from django.db import models
from users.models import User, BaseModel


QUESTION_TYPES = (
    ('YN', 'Yes/No'),
)

ANSWER = (
    ('YES', 'YES'),
    ('NO', 'NO'),
    ('MAYBE', 'MAYBE')
)


class InfoOption(models.Model):
    """
    Accept info at this options
    """
    info_at = models.CharField(max_length=10)

    def __str__(self):
        return self.info_at


class Question(BaseModel):
    """
    The actual question text and its type
    """
    question_text = models.TextField()
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="sub_questions")
    order = models.CharField(max_length=3, null=True, blank=True)
    options = models.IntegerField(default=2)
    info_required = models.BooleanField(default=False)
    info_at = models.ManyToManyField(InfoOption, related_name="info_at_options", null=True, blank=True)
    follow_up = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question_text

    @property
    def custom_order(self):
        """
        Returns prder of questions
        """
        if self.parent_question:
            return self.parent_question.order + '.' + self.order

        return self.order


class UserQuestionnaire(BaseModel):
    """
    Tracks the user taking the test and the date of the test
    """
    token_id = models.UUIDField(unique=True, default=uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_questionnaires")
    test_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Test for {self.user.username} on {self.test_date}"

    @property
    def created(self):
        """
        Returns total clips for each episode
        """
        return self.created_at

    @property
    def yes_answers(self):
        """Returns all the yes answers"""
        return self.questionnaire_answers.filter(yes_no_answer=True)


class Answer(BaseModel):
    """
    Stores the user's answer to a particular question
    """
    user_questionnaire = models.ForeignKey(UserQuestionnaire, on_delete=models.CASCADE, related_name="questionnaire_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questionnaire_questions")
    yes_no_answer = models.CharField(max_length=10, choices=ANSWER, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.user_questionnaire.user.username}"


class Activity(BaseModel):
    """
    User activity
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(UserQuestionnaire, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} activity"
