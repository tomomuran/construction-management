from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Schedule(models.Model):
    STATUS_CHOICES = [
        ("not_started", "未着手"),
        ("in_progress", "進行中"),
        ("completed", "完了"),
        ("delayed", "遅延"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="プロジェクト",
    )
    task_name = models.CharField("作業項目", max_length=200)
    planned_start_date = models.DateField("開始予定日")
    planned_end_date = models.DateField("終了予定日")
    actual_start_date = models.DateField("実際の開始日", null=True, blank=True)
    actual_end_date = models.DateField("実際の終了日", null=True, blank=True)
    status = models.CharField(
        "状況", max_length=20, choices=STATUS_CHOICES, default="not_started"
    )
    progress = models.IntegerField("進捗率", default=0)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="担当者"
    )
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "工程"
        verbose_name_plural = "工程"
        ordering = ["planned_start_date", "planned_end_date"]

    def __str__(self):
        return f"{self.project.name} - {self.task_name}"

    @property
    def is_delayed(self):
        if (
            not self.actual_end_date
            and self.planned_end_date < models.timezone.now().date()
        ):
            return True
        return False
