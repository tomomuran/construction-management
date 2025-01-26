from django.db import models
from django.core.validators import MinValueValidator
from projects.models import Project


class MaterialCategory(models.Model):
    """資材カテゴリ（建材、工具、消耗品など）"""

    name = models.CharField("カテゴリ名", max_length=100)
    description = models.TextField("説明", blank=True)

    class Meta:
        verbose_name = "資材カテゴリ"
        verbose_name_plural = "資材カテゴリ"

    def __str__(self):
        return self.name


class Material(models.Model):
    """資材情報"""

    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name="カテゴリ",
    )
    name = models.CharField("資材名", max_length=200)
    code = models.CharField("資材コード", max_length=50, unique=True)
    specification = models.CharField("規格", max_length=200, blank=True)
    unit = models.CharField("単位", max_length=50)
    unit_price = models.DecimalField(
        "単価", max_digits=12, decimal_places=0, validators=[MinValueValidator(0)]
    )
    current_stock = models.DecimalField(
        "現在の在庫数", max_digits=10, decimal_places=2, default=0
    )
    minimum_stock = models.DecimalField(
        "最小在庫数", max_digits=10, decimal_places=2, default=0
    )
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "資材"
        verbose_name_plural = "資材"
        ordering = ["category", "code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def stock_status(self):
        """在庫状況を判定"""
        if self.current_stock <= 0:
            return "out_of_stock"  # 在庫切れ
        elif self.current_stock <= self.minimum_stock:
            return "low_stock"  # 要発注
        return "in_stock"  # 在庫あり


class MaterialTransaction(models.Model):
    """資材の入出庫記録"""

    TRANSACTION_TYPES = [
        ("in", "入庫"),
        ("out", "出庫"),
    ]

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="資材",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="material_transactions",
        verbose_name="プロジェクト",
    )
    transaction_type = models.CharField(
        "取引種類", max_length=3, choices=TRANSACTION_TYPES
    )
    quantity = models.DecimalField(
        "数量", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    unit_price = models.DecimalField(
        "取引単価", max_digits=12, decimal_places=0, validators=[MinValueValidator(0)]
    )
    transaction_date = models.DateField("取引日")
    order_number = models.CharField("発注番号", max_length=100, blank=True)
    delivery_number = models.CharField("納品番号", max_length=100, blank=True)
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "資材取引"
        verbose_name_plural = "資材取引"
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.material.name} - {self.get_transaction_type_display()} - {self.quantity}{self.material.unit}"

    def save(self, *args, **kwargs):
        """在庫数を更新"""
        if not self.pk:  # 新規作成時のみ
            if self.transaction_type == "in":
                self.material.current_stock += self.quantity
            else:  # out
                self.material.current_stock -= self.quantity
            self.material.save()
        super().save(*args, **kwargs)
