from django.db import models
from django.core.validators import MinValueValidator
from projects.models import Project


class CostCategory(models.Model):
    """原価カテゴリモデル"""

    name = models.CharField("カテゴリ名", max_length=50)
    description = models.TextField("説明", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "原価カテゴリ"
        verbose_name_plural = "原価カテゴリ"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cost(models.Model):
    """原価モデル"""

    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "未払い"),
        ("partially_paid", "一部支払済"),
        ("paid", "支払済"),
    ]

    project = models.ForeignKey(
        Project,
        verbose_name="プロジェクト",
        on_delete=models.CASCADE,
        related_name="costs",
    )
    category = models.ForeignKey(
        CostCategory,
        verbose_name="カテゴリ",
        on_delete=models.PROTECT,
        related_name="costs",
    )
    item_name = models.CharField("項目名", max_length=100)
    planned_amount = models.DecimalField(
        "予算金額", max_digits=12, decimal_places=0, validators=[MinValueValidator(0)]
    )
    actual_amount = models.DecimalField(
        "実績金額",
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    payment_status = models.CharField(
        "支払状況", max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid"
    )
    payment_date = models.DateField("支払日", null=True, blank=True)
    invoice_number = models.CharField("請求書番号", max_length=50, blank=True)
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "原価"
        verbose_name_plural = "原価"
        ordering = ["-payment_date", "-created_at"]

    def __str__(self):
        return f"{self.project.name} - {self.category.name} - {self.item_name}"

    @property
    def variance_amount(self):
        """予実差額を計算"""
        if self.actual_amount is None:
            return None
        return self.planned_amount - self.actual_amount

    @property
    def variance_rate(self):
        """予実差額率を計算"""
        if self.actual_amount is None or self.planned_amount == 0:
            return None
        return (self.variance_amount / self.planned_amount) * 100
