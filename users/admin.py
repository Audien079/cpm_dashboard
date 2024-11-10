from django.contrib import admin
from users.models import User, Task, Setting


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User data view in admin panel
    """

    list_display = ["id", "username", "email"]
    search_fields = ["username", "email"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Task data view in admin panel
    """

    list_display = ["name", "client", "due_date"]
    search_fields = ["name", "client"]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """
    Setting data view in admin panel
    """

    list_display = ["first_survey_date", "second_survey_date", "send_followups", "follow_cycle"]
