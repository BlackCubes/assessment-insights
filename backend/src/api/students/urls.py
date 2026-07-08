from django.urls import path

from .views import StudentDetailUpdateView, StudentListCreateView

urlpatterns = [
    path("", StudentListCreateView.as_view(), name="student-list-create"),
    path("<uuid:uuid>/", StudentDetailUpdateView.as_view(), name="student-detail-update"),
    path("<int:student_id>/", StudentDetailUpdateView.as_view(), name="student-detail-update"),
]
