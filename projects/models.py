from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField("プロジェクト名", max_length=200)
    location = models.CharField("現場所在地", max_length=200)
    start_date = models.DateField("着工日")
    end_date = models.DateField("竣工予定日")
    description = models.TextField("工事概要", blank=True)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="現場監督")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "工事プロジェクト"
        verbose_name_plural = "工事プロジェクト"
