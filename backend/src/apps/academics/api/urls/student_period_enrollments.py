from django.urls import path

from apps.academics.api.views import (
    StudentPeriodEnrollmentDetailView,
    StudentPeriodEnrollmentListCreateView,
)

app_name = "enrollments"

urlpatterns = [
    path("", StudentPeriodEnrollmentListCreateView.as_view(), name="list-create"),
    path("<uuid:uuid>/", StudentPeriodEnrollmentDetailView.as_view(), name="detail"),
]
