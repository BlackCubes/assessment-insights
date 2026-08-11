from django.urls import path

from apps.students.api.views import StudentDetailView, StudentListCreateView

urlpatterns = [
    path("", StudentListCreateView.as_view(), name="list-create"),
    path("<uuid:uuid>/", StudentDetailView.as_view(), name="detail"),
    path(
        "<int:student_id>/",
        StudentDetailView.as_view(),
        name="detail",
    ),
]
