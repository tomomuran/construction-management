from django.urls import path
from . import views

app_name = "materials"

urlpatterns = [
    # 資材関連
    path("materials/", views.MaterialListView.as_view(), name="material_list"),
    path(
        "materials/create/", views.MaterialCreateView.as_view(), name="material_create"
    ),
    path(
        "materials/<int:pk>/",
        views.MaterialDetailView.as_view(),
        name="material_detail",
    ),
    path(
        "materials/<int:pk>/update/",
        views.MaterialUpdateView.as_view(),
        name="material_update",
    ),
    path(
        "materials/<int:pk>/delete/",
        views.MaterialDeleteView.as_view(),
        name="material_delete",
    ),
    # 取引関連
    path("transactions/", views.TransactionListView.as_view(), name="transaction_list"),
    path(
        "materials/<int:material_id>/transactions/",
        views.TransactionListView.as_view(),
        name="material_transactions",
    ),
    path(
        "materials/<int:material_id>/transactions/create/",
        views.TransactionCreateView.as_view(),
        name="transaction_create",
    ),
    path(
        "transactions/<int:pk>/update/",
        views.TransactionUpdateView.as_view(),
        name="transaction_update",
    ),
]
