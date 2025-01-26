from django.urls import path
from . import views

app_name = "schedules"

urlpatterns = [
    # 全体のスケジュール一覧
    path("", views.ScheduleListView.as_view(), name="schedule_list"),
    # プロジェクト別のスケジュール一覧と作成
    path(
        "project/<int:project_id>/",
        views.ScheduleListView.as_view(),
        name="project_schedules",
    ),
    path(
        "project/<int:project_id>/create/",
        views.ScheduleCreateView.as_view(),
        name="schedule_create",
    ),
    # 個別のスケジュール詳細、編集、削除
    path("<int:pk>/", views.ScheduleDetailView.as_view(), name="schedule_detail"),
    path(
        "<int:pk>/update/", views.ScheduleUpdateView.as_view(), name="schedule_update"
    ),
    path(
        "<int:pk>/delete/", views.ScheduleDeleteView.as_view(), name="schedule_delete"
    ),
]
