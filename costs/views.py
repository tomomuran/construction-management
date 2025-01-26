from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from projects.models import Project
from .models import Cost, CostCategory


class CostListView(LoginRequiredMixin, ListView):
    model = Cost
    template_name = "costs/cost_list.html"
    context_object_name = "costs"
    ordering = ["-payment_date", "-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.kwargs.get("project_id")
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("project_id")

        if project_id:
            project = get_object_or_404(Project, pk=project_id)
            context["project"] = project

            # カテゴリごとの集計
            costs_by_category = []
            categories = CostCategory.objects.all()

            for category in categories:
                category_costs = Cost.objects.filter(project=project, category=category)
                planned_total = (
                    category_costs.aggregate(total=Sum("planned_amount"))["total"] or 0
                )
                actual_total = (
                    category_costs.aggregate(total=Sum("actual_amount"))["total"] or 0
                )

                costs_by_category.append(
                    {
                        "category": category,
                        "planned_total": planned_total,
                        "actual_total": actual_total,
                        "variance": (
                            planned_total - actual_total if actual_total else None
                        ),
                    }
                )

            context["costs_by_category"] = costs_by_category

            # 全体の集計
            total_planned = sum(item["planned_total"] for item in costs_by_category)
            total_actual = sum(item["actual_total"] for item in costs_by_category)

            context["total_planned"] = total_planned
            context["total_actual"] = total_actual

        return context


class CostDetailView(LoginRequiredMixin, DetailView):
    model = Cost
    template_name = "costs/cost_detail.html"
    context_object_name = "cost"


class CostCreateView(LoginRequiredMixin, CreateView):
    model = Cost
    template_name = "costs/cost_form.html"
    fields = [
        "category",
        "item_name",
        "planned_amount",
        "actual_amount",
        "payment_status",
        "payment_date",
        "invoice_number",
        "notes",
    ]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.project = get_object_or_404(Project, pk=kwargs["project_id"])

    def form_valid(self, form):
        form.instance.project = self.project
        messages.success(self.request, "原価情報を登録しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("costs:cost_detail", kwargs={"pk": self.object.pk})


class CostUpdateView(LoginRequiredMixin, UpdateView):
    model = Cost
    template_name = "costs/cost_form.html"
    fields = [
        "category",
        "item_name",
        "planned_amount",
        "actual_amount",
        "payment_status",
        "payment_date",
        "invoice_number",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "原価情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("costs:cost_detail", kwargs={"pk": self.object.pk})


class CostDeleteView(LoginRequiredMixin, DeleteView):
    model = Cost
    template_name = "costs/cost_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "原価情報を削除しました。")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "costs:project_costs", kwargs={"project_id": self.object.project.id}
        )
