from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "task_name",
        "planned_start_date",
        "planned_end_date",
        "status",
        "progress",
        "assigned_to",
    )
    list_filter = ("project", "status", "assigned_to")
    search_fields = ("task_name", "project__name")
    date_hierarchy = "planned_start_date"
