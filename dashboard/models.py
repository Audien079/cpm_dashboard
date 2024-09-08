from uuid import uuid4
from django.db import models
from users.models import User, BaseModel


QUESTION_TYPES = (
    ('YN', 'Yes/No'),
    ('TEXT', 'Input'),
)


class Question(BaseModel):
    """
    The actual question text and its type
    """
    question_text = models.TextField()
    type_name = models.CharField(max_length=4, choices=QUESTION_TYPES)

    def __str__(self):
        return self.question_text


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


class Answer(BaseModel):
    """
    Stores the user's answer to a particular question
    """
    user_questionnaire = models.ForeignKey(UserQuestionnaire, on_delete=models.CASCADE, related_name="questionnaire_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questionnaire_questions")

    # Answers based on the type of question:
    yes_no_answer = models.BooleanField(null=True, blank=True)  # For Yes/No type questions
    text_answer = models.TextField(null=True, blank=True)  # For text input answers

    def save(self, *args, **kwargs):
        if self.question.type_name == 'YN':
            self.text_answer = None

        elif self.question.type_name == 'TEXT':
            self.yes_no_answer = None

        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return f"Answer to {self.question} by {self.user_questionnaire.user.username}"
