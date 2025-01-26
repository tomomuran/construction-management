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
from .models import Schedule
from projects.models import Project

# Create your views here.


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = "schedules/schedule_list.html"
    context_object_name = "schedules"
    ordering = ["planned_start_date"]

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
            context["project"] = get_object_or_404(Project, pk=project_id)
        return context


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule
    template_name = "schedules/schedule_detail.html"


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    template_name = "schedules/schedule_form.html"
    fields = [
        "task_name",
        "planned_start_date",
        "planned_end_date",
        "actual_start_date",
        "actual_end_date",
        "status",
        "progress",
        "assigned_to",
        "notes",
    ]

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        form.instance.project = project
        messages.success(self.request, "スケジュールを登録しました。")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return context

    def get_success_url(self):
        return reverse_lazy(
            "schedules:project_schedules",
            kwargs={"project_id": self.kwargs["project_id"]},
        )


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    template_name = "schedules/schedule_form.html"
    fields = [
        "task_name",
        "planned_start_date",
        "planned_end_date",
        "actual_start_date",
        "actual_end_date",
        "status",
        "progress",
        "assigned_to",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "スケジュール情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "schedules:project_schedules", kwargs={"project_id": self.object.project.id}
        )


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    template_name = "schedules/schedule_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "スケジュールを削除しました。")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "schedules:project_schedules", kwargs={"project_id": self.object.project.id}
        )
