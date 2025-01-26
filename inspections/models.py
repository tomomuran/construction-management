from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Inspection(models.Model):
    INSPECTION_TYPES = [
        ("regular", "定期検査"),
        ("special", "臨時検査"),
        ("completion", "完了検査"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="プロジェクト"
    )
    inspection_date = models.DateField("検査日")
    inspection_type = models.CharField(
        "検査種類", max_length=20, choices=INSPECTION_TYPES
    )
    inspector = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="検査員")
    location = models.CharField("検査箇所", max_length=200)
    findings = models.TextField("検査内容・指摘事項")
    status = models.CharField(
        "状態",
        max_length=20,
        choices=[
            ("pending", "対応待ち"),
            ("in_progress", "対応中"),
            ("completed", "完了"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.get_inspection_type_display()} ({self.inspection_date})"

    class Meta:
        verbose_name = "検査記録"
        verbose_name_plural = "検査記録"
