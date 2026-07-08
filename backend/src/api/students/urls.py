from django.urls import path

from .views import StudentDetailView, StudentListCreateView

urlpatterns = [
    path("", StudentListCreateView.as_view(), name="student-list-create"),
    path("<uuid:uuid>/", StudentDetailView.as_view(), name="student-detail"),
    path("<int:student_id>/", StudentDetailView.as_view(), name="student-detail"),
]
