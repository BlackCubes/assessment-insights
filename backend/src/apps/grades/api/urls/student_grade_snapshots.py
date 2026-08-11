from django.urls import path

from apps.grades.api.views import (
    StudentGradeSnapshotDetailView,
    StudentGradeSnapshotListCreateView,
)

urlpatterns = [
    path("", StudentGradeSnapshotListCreateView.as_view(), name="list-create"),
    path("<uuid:uuid>/", StudentGradeSnapshotDetailView.as_view(), name="detail"),
]
