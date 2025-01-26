from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project
from django.db.models import Sum


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    ordering = ["-created_at"]


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # スケジュール情報を取得
        context["schedules"] = self.object.schedules.all().order_by(
            "planned_start_date", "planned_end_date"
        )[:5]
        # コスト情報を取得
        context["costs"] = self.object.costs.all().order_by("-payment_date")[:5]
        # 合計コストを計算
        total_costs = self.object.costs.aggregate(
            total_planned=Sum("planned_amount"), total_actual=Sum("actual_amount")
        )
        context["total_planned_cost"] = total_costs["total_planned"] or 0
        context["total_actual_cost"] = total_costs["total_actual"] or 0
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "projects/project_form.html"
    fields = ["name", "location", "start_date", "end_date", "description", "manager"]

    def form_valid(self, form):
        messages.success(self.request, "プロジェクトを作成しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("projects:project_detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "projects/project_form.html"
    fields = ["name", "location", "start_date", "end_date", "description", "manager"]

    def form_valid(self, form):
        messages.success(self.request, "プロジェクト情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("projects:project_detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:project_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "プロジェクトを削除しました。")
        return super().delete(request, *args, **kwargs)
