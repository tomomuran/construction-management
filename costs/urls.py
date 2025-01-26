from django.urls import path
from . import views

app_name = "costs"

urlpatterns = [
    path("", views.CostListView.as_view(), name="cost_list"),
    path(
        "project/<int:project_id>/", views.CostListView.as_view(), name="project_costs"
    ),
    path(
        "project/<int:project_id>/create/",
        views.CostCreateView.as_view(),
        name="cost_create",
    ),
    path("<int:pk>/", views.CostDetailView.as_view(), name="cost_detail"),
    path("<int:pk>/update/", views.CostUpdateView.as_view(), name="cost_update"),
    path("<int:pk>/delete/", views.CostDeleteView.as_view(), name="cost_delete"),
]
