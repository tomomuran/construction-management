from django.db import models
from django.core.validators import MinValueValidator
from projects.models import Project

# Create your models here.


class Worker(models.Model):
    """作業員情報"""

    EMPLOYMENT_STATUS_CHOICES = [
        ("full_time", "正社員"),
        ("contract", "契約社員"),
        ("part_time", "パート"),
        ("temporary", "派遣"),
    ]

    name = models.CharField("氏名", max_length=100)
    employee_number = models.CharField("社員番号", max_length=50, unique=True)
    phone_number = models.CharField("電話番号", max_length=20)
    email = models.EmailField("メールアドレス", blank=True)
    address = models.TextField("住所")
    employment_status = models.CharField(
        "雇用形態", max_length=20, choices=EMPLOYMENT_STATUS_CHOICES
    )
    join_date = models.DateField("入社日")
    leave_date = models.DateField("退社日", null=True, blank=True)
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "作業員"
        verbose_name_plural = "作業員"
        ordering = ["employee_number"]

    def __str__(self):
        return f"{self.employee_number} - {self.name}"

    @property
    def is_active(self):
        """在籍中かどうかを判定"""
        return self.leave_date is None


class Qualification(models.Model):
    """資格情報"""

    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name="qualifications",
        verbose_name="作業員",
    )
    name = models.CharField("資格名", max_length=100)
    qualification_number = models.CharField("資格番号", max_length=100)
    issue_date = models.DateField("取得日")
    expiry_date = models.DateField("有効期限", null=True, blank=True)
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "資格"
        verbose_name_plural = "資格"
        ordering = ["worker", "-issue_date"]

    def __str__(self):
        return f"{self.worker.name} - {self.name}"

    @property
    def is_valid(self):
        """有効期限内かどうかを判定"""
        if not self.expiry_date:
            return True
        from django.utils import timezone

        return self.expiry_date >= timezone.now().date()


class WorkRecord(models.Model):
    """作業記録"""

    worker = models.ForeignKey(
        Worker,
        on_delete=models.PROTECT,
        related_name="work_records",
        verbose_name="作業員",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="work_records",
        verbose_name="プロジェクト",
    )
    work_date = models.DateField("作業日")
    start_time = models.TimeField("開始時間")
    end_time = models.TimeField("終了時間")
    break_time = models.PositiveIntegerField(
        "休憩時間（分）", default=60, validators=[MinValueValidator(0)]
    )
    work_description = models.TextField("作業内容")
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "作業記録"
        verbose_name_plural = "作業記録"
        ordering = ["-work_date", "-start_time"]

    def __str__(self):
        return f"{self.worker.name} - {self.work_date} - {self.project.name}"

    @property
    def working_hours(self):
        """実労働時間を計算（時間）"""
        from datetime import datetime, timedelta

        start = datetime.combine(self.work_date, self.start_time)
        end = datetime.combine(self.work_date, self.end_time)
        total_minutes = (end - start).total_seconds() / 60 - self.break_time
        return round(total_minutes / 60, 2)
