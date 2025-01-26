from django.contrib import admin
from django.urls import path, include
from accounts.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("projects/", include("projects.urls")),
    path("schedules/", include("schedules.urls")),
    path("costs/", include("costs.urls")),
    path("materials/", include("materials.urls")),
    path("workers/", include("workers.urls")),
    path("accounts/", include("accounts.urls")),
]
