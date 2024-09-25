from admin import logger
from datetime import datetime
from django.db.models.signals import post_save

from dashboard.models import UserQuestionnaire


def questionnaire_post_save(instance, *args, **kwargs):
    """
    Questionnaire post save
    """
    try:
        if instance:
            user = instance.user
            user.last_contacted = datetime.now()
            user.save()
    except Exception as e:
        logger.exception(msg=str(e), exc_info=True)


post_save.connect(questionnaire_post_save, sender=UserQuestionnaire)
