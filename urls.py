from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="projects:project_list"), name="index"),
    path("projects/", include("projects.urls")),
    path("schedules/", include("schedules.urls")),
    path("costs/", include("costs.urls")),
    path("materials/", include("materials.urls")),
    path("workers/", include("workers.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
