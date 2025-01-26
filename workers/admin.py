from django.contrib import admin
from .models import Worker, Qualification, WorkRecord


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        "employee_number",
        "name",
        "employment_status",
        "phone_number",
        "join_date",
        "is_active",
    )
    list_filter = ("employment_status", "join_date")
    search_fields = ("name", "employee_number", "phone_number", "email")
    date_hierarchy = "join_date"


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = (
        "worker",
        "name",
        "qualification_number",
        "issue_date",
        "expiry_date",
        "is_valid",
    )
    list_filter = ("name", "issue_date")
    search_fields = ("worker__name", "name", "qualification_number")
    date_hierarchy = "issue_date"


@admin.register(WorkRecord)
class WorkRecordAdmin(admin.ModelAdmin):
    list_display = (
        "work_date",
        "worker",
        "project",
        "start_time",
        "end_time",
        "break_time",
        "working_hours",
    )
    list_filter = ("work_date", "worker", "project")
    search_fields = ("worker__name", "project__name", "work_description")
    date_hierarchy = "work_date"
