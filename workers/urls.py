from django.urls import path
from . import views

app_name = "workers"

urlpatterns = [
    # 作業員関連
    path("", views.WorkerListView.as_view(), name="worker_list"),
    path("create/", views.WorkerCreateView.as_view(), name="worker_create"),
    path("<int:pk>/", views.WorkerDetailView.as_view(), name="worker_detail"),
    path("<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker_update"),
    path("<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="worker_delete"),
    # 資格関連
    path(
        "<int:worker_id>/qualifications/create/",
        views.QualificationCreateView.as_view(),
        name="qualification_create",
    ),
    path(
        "qualifications/<int:pk>/update/",
        views.QualificationUpdateView.as_view(),
        name="qualification_update",
    ),
    # 作業記録関連
    path(
        "<int:worker_id>/work-records/create/",
        views.WorkRecordCreateView.as_view(),
        name="work_record_create",
    ),
    path(
        "work-records/<int:pk>/update/",
        views.WorkRecordUpdateView.as_view(),
        name="work_record_update",
    ),
]
