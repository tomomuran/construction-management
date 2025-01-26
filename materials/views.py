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
from .models import Material, MaterialCategory, MaterialTransaction
from projects.models import Project

# Create your views here.


class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    template_name = "materials/material_list.html"
    context_object_name = "materials"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = MaterialCategory.objects.all()
        return context


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    template_name = "materials/material_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.get_object()

        # 最近の取引履歴を取得
        context["recent_transactions"] = material.transactions.all()[:10]

        # 在庫推移を計算（月次）
        transactions = material.transactions.all()
        context["stock_history"] = (
            transactions.values("transaction_date__month")
            .annotate(
                total_in=Sum("quantity", filter=Q(transaction_type="in")),
                total_out=Sum("quantity", filter=Q(transaction_type="out")),
            )
            .order_by("transaction_date__month")
        )

        return context


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    template_name = "materials/material_form.html"
    fields = [
        "category",
        "name",
        "code",
        "specification",
        "unit",
        "unit_price",
        "current_stock",
        "minimum_stock",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "資材を登録しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("materials:material_detail", kwargs={"pk": self.object.pk})


class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    template_name = "materials/material_form.html"
    fields = [
        "category",
        "name",
        "code",
        "specification",
        "unit",
        "unit_price",
        "minimum_stock",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "資材情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("materials:material_detail", kwargs={"pk": self.object.pk})


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = "materials/material_confirm_delete.html"
    success_url = reverse_lazy("materials:material_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "資材を削除しました。")
        return super().delete(request, *args, **kwargs)


class TransactionListView(LoginRequiredMixin, ListView):
    model = MaterialTransaction
    template_name = "materials/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        queryset = MaterialTransaction.objects.all()
        material_id = self.kwargs.get("material_id")
        if material_id:
            queryset = queryset.filter(material_id=material_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material_id = self.kwargs.get("material_id")
        if material_id:
            context["material"] = get_object_or_404(Material, id=material_id)
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = MaterialTransaction
    template_name = "materials/transaction_form.html"
    fields = [
        "material",
        "project",
        "transaction_type",
        "quantity",
        "unit_price",
        "transaction_date",
        "order_number",
        "delivery_number",
        "notes",
    ]

    def get_initial(self):
        initial = super().get_initial()
        material_id = self.kwargs.get("material_id")
        if material_id:
            material = get_object_or_404(Material, id=material_id)
            initial["material"] = material
            initial["unit_price"] = material.unit_price
        return initial

    def form_valid(self, form):
        messages.success(self.request, "取引を記録しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "materials:material_detail", kwargs={"pk": self.object.material.pk}
        )


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = MaterialTransaction
    template_name = "materials/transaction_form.html"
    fields = [
        "project",
        "transaction_type",
        "quantity",
        "unit_price",
        "transaction_date",
        "order_number",
        "delivery_number",
        "notes",
    ]

    def form_valid(self, form):
        messages.success(self.request, "取引情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "materials:material_detail", kwargs={"pk": self.object.material.pk}
        )
