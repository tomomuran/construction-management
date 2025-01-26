from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.utils import timezone
from .models import Worker, Qualification, WorkRecord
from projects.models import Project

# Create your views here.


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "workers/worker_list.html"
    context_object_name = "workers"

    def get_queryset(self):
        queryset = Worker.objects.all()
        status = self.request.GET.get("status")
        if status == "active":
            queryset = queryset.filter(leave_date__isnull=True)
        elif status == "inactive":
            queryset = queryset.filter(leave_date__isnull=False)
        return queryset


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "workers/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()

        # 資格情報を取得
        context["qualifications"] = worker.qualifications.all()

        # 最近の作業記録を取得
        context["recent_work_records"] = worker.work_records.all()[:10]

        # 月間の作業時間を集計
        today = timezone.now().date()
        first_day = today.replace(day=1)
        monthly_records = worker.work_records.filter(work_date__gte=first_day)

        total_hours = 0
        for record in monthly_records:
            total_hours += record.working_hours

        context["monthly_hours"] = total_hours

        return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    template_name = "workers/worker_form.html"
    fields = [
        "name",
        "employee_number",
        "phone_number",
        "email",
        "address",
        "employment_status",
        "join_date",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "作業員を登録しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workers:worker_detail", kwargs={"pk": self.object.pk})


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    template_name = "workers/worker_form.html"
    fields = [
        "name",
        "phone_number",
        "email",
        "address",
        "employment_status",
        "leave_date",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "作業員情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workers:worker_detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    template_name = "workers/worker_confirm_delete.html"
    success_url = reverse_lazy("workers:worker_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "作業員を削除しました。")
        return super().delete(request, *args, **kwargs)


class QualificationCreateView(LoginRequiredMixin, CreateView):
    model = Qualification
    template_name = "workers/qualification_form.html"
    fields = ["name", "qualification_number", "issue_date", "expiry_date", "notes"]

    def form_valid(self, form):
        worker = get_object_or_404(Worker, pk=self.kwargs["worker_id"])
        form.instance.worker = worker
        messages.success(self.request, "資格を登録しました。")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker"] = get_object_or_404(Worker, pk=self.kwargs["worker_id"])
        return context

    def get_success_url(self):
        return reverse_lazy(
            "workers:worker_detail", kwargs={"pk": self.kwargs["worker_id"]}
        )


class QualificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Qualification
    template_name = "workers/qualification_form.html"
    fields = ["name", "qualification_number", "issue_date", "expiry_date", "notes"]

    def form_valid(self, form):
        messages.success(self.request, "資格情報を更新しました。")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker"] = self.object.worker
        return context

    def get_success_url(self):
        return reverse_lazy(
            "workers:worker_detail", kwargs={"pk": self.object.worker.pk}
        )


class WorkRecordCreateView(LoginRequiredMixin, CreateView):
    model = WorkRecord
    template_name = "workers/work_record_form.html"
    fields = [
        "project",
        "work_date",
        "start_time",
        "end_time",
        "break_time",
        "work_description",
        "notes",
    ]

    def form_valid(self, form):
        worker = get_object_or_404(Worker, pk=self.kwargs["worker_id"])
        form.instance.worker = worker
        messages.success(self.request, "作業記録を登録しました。")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker"] = get_object_or_404(Worker, pk=self.kwargs["worker_id"])
        return context

    def get_success_url(self):
        return reverse_lazy(
            "workers:worker_detail", kwargs={"pk": self.kwargs["worker_id"]}
        )


class WorkRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkRecord
    template_name = "workers/work_record_form.html"
    fields = [
        "project",
        "work_date",
        "start_time",
        "end_time",
        "break_time",
        "work_description",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "作業記録を更新しました。")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker"] = self.object.worker
        return context

    def get_success_url(self):
        return reverse_lazy(
            "workers:worker_detail", kwargs={"pk": self.object.worker.pk}
        )
