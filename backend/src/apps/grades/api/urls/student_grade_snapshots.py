from django.urls import path

from apps.grades.api.views import (
    StudentGradeSnapshotBulkCreateView,
    StudentGradeSnapshotDetailView,
    StudentGradeSnapshotListCreateView,
)

urlpatterns = [
    path("", StudentGradeSnapshotListCreateView.as_view(), name="list-create"),
    path("bulk/", StudentGradeSnapshotBulkCreateView.as_view(), name="bulk-create"),
    path("<uuid:uuid>/", StudentGradeSnapshotDetailView.as_view(), name="detail"),
]
